"""Selects, renders, post-processes, diffs and (optionally) publishes screenshots.

Default is a dry run: previews, cache and last-run.json only.
  --apply   local lock, doc and cache writes; no network
  --upload  implies --apply and allows the CDN upload
  --recover completes pending transactions without rendering or network

Exit codes: 0 all fine, 1 refused/failed/baseline-unavailable, 2 usage,
3 a conflict, upload-unknown or artifact-corrupt is pending.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import diff as diffmod
import docrefs
import gitutil
import txn as txnmod
import upload
from apply import Conflict, apply_doc, apply_lock, doc_sha256, read_lock
from check import (DIRTY_SOURCES, ORPHAN, PLATFORM_MISMATCH, STALE, CheckContext, entry_row)
from common import (DEFAULT_CACHE, DEFAULT_LOCK, DEFAULT_MANIFEST, MANUAL_ROOT, PipelineError,
                    UsageError, atomic_write_json, dedupe, split_ids, utc_now_iso)
from manifest import Entry, Manifest, inputs_hash, load_manifest
from postprocess import PostprocessError, process, processing_descriptor
from render import RenderConfig, Renderer, comparable_json, freshness_warnings

OK_STATUSES = ("updated", "unchanged", "lock-advanced", "unchanged-lock-not-advanced", "would-replace")
PENDING_STATUSES = ("conflict", "upload-unknown", "artifact-corrupt")
PREVIEW_STATUSES = ("preview-only-dirty", "preview-only-platform")


@dataclass
class EntryResult:
    id: str
    status: str
    details: dict[str, Any] = field(default_factory=dict)
    # Printed to the terminal only: capability URLs never reach a file.
    del_url: Optional[str] = None

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "status": self.status, "details": self.details}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Render and publish manual screenshots.")
    p.add_argument("--gpgfrontend", type=Path, help="GpgFrontend repository")
    p.add_argument("--binary", type=Path, help="screenshot-mode binary (else $GF_SCREENSHOT_BINARY)")
    p.add_argument("--only", help="comma separated entry ids (default: every renderable entry)")
    p.add_argument("--force", action="store_true", help="select every candidate, stale or not")
    p.add_argument("--accept-baseline", default="", help="ids whose baseline is unavailable: replace anyway")
    p.add_argument("--force-replace", default="", help="ids to replace whatever the diff says")
    p.add_argument("--allow-dirty", action="store_true", help="render dirty entries as previews only")
    p.add_argument("--apply", action="store_true", help="write lock, docs and cache (no network)")
    p.add_argument("--upload", action="store_true", help="implies --apply; upload replacements")
    p.add_argument("--repeat", type=int, default=None, help="render N times and require identical bytes")
    p.add_argument("--recover", action="store_true", help="complete pending transactions only")
    p.add_argument("--resolve", metavar="TXN_ID", help="with --recover: decide an upload-unknown transaction")
    p.add_argument("--url", help="with --resolve: the URL found in the EasyImages admin")
    p.add_argument("--retry-upload", action="store_true", help="with --resolve: upload again (may duplicate)")
    p.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    p.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    p.add_argument("--manual-root", type=Path, default=MANUAL_ROOT)
    p.add_argument("--work-root", type=Path, help="throwaway directory root (default /tmp/gf-shot-<uid>)")
    p.add_argument("--keep-work", action="store_true", help="keep throwaway directories for debugging")
    return p


def validate_flags(args: argparse.Namespace) -> None:
    if args.recover:
        clashes = [name for name, on in (
            ("--only", args.only is not None), ("--force", args.force),
            ("--accept-baseline", bool(args.accept_baseline)), ("--force-replace", bool(args.force_replace)),
            ("--repeat", args.repeat is not None)) if on]
        if clashes:
            raise UsageError(f"--recover cannot be combined with {', '.join(clashes)}")
    else:
        if args.resolve:
            raise UsageError("--resolve needs --recover")
        if not args.gpgfrontend:
            raise UsageError("--gpgfrontend is required")
    if (args.url or args.retry_upload) and not args.resolve:
        raise UsageError("--url and --retry-upload need --resolve")
    if args.resolve and bool(args.url) == bool(args.retry_upload):
        raise UsageError("--resolve needs exactly one of --url or --retry-upload")
    if args.repeat is not None and args.repeat < 1:
        raise UsageError("--repeat must be at least 1")
    both = set(split_ids(args.accept_baseline)) & set(split_ids(args.force_replace))
    if both:
        raise UsageError(f"id(s) in both --accept-baseline and --force-replace: {', '.join(sorted(both))}")


def candidates(manifest: Manifest, only: Optional[str]) -> list[Entry]:
    by_id = manifest.by_id()
    if only is None:
        return [e for e in manifest.entries if e.renderable]
    ids = split_ids(only)
    if not ids:
        raise UsageError("--only needs at least one id")
    out = []
    for entry_id in dedupe(ids):
        if entry_id not in by_id:
            raise UsageError(f"unknown id: {entry_id}")
        if not by_id[entry_id].renderable:
            raise UsageError(f"{entry_id} is {by_id[entry_id].status} and is never rendered")
        out.append(by_id[entry_id])
    return out


def validate_overrides(args: argparse.Namespace, selected: set[str], lock: dict[str, Any],
                       cache: Path) -> tuple[set[str], set[str]]:
    accept = set(split_ids(args.accept_baseline))
    force = set(split_ids(args.force_replace))
    for entry_id in sorted(accept | force):
        if entry_id not in selected:
            raise UsageError(f"{entry_id} is not selected in this run; overrides apply to selected ids only")
    for entry_id in sorted(accept):
        record = lock.get(entry_id)
        if not record:
            raise UsageError(f"--accept-baseline {entry_id}: no lock record, so the result is new, "
                             "not baseline-unavailable")
        if diffmod.baseline_valid(cache, entry_id, record):
            raise UsageError(f"--accept-baseline {entry_id}: the baseline is valid; use --force-replace "
                             "to replace it anyway")
    return accept, force


class Runner:
    def __init__(self, args: argparse.Namespace, manifest: Manifest, renderer: Renderer,
                 creds: Optional[upload.Credentials]) -> None:
        self.args = args
        self.manifest = manifest
        self.renderer = renderer
        self.creds = creds
        self.cache: Path = args.cache
        self.apply = args.apply or args.upload
        self.paths = txnmod.Paths(Path(args.manual_root), Path(args.lock), self.cache)
        self.warnings: list[str] = []
        self.stop_txn = False
        self.head = gitutil.head(args.gpgfrontend)
        self.processing = processing_descriptor()

    # Rendering -------------------------------------------------------------

    def render_repeated(self, entry: Entry) -> tuple[Any, Optional[str]]:
        repeat = self.args.repeat or 1
        outcomes = []
        for i in range(repeat):
            outcome = self.renderer.render(entry, self.cache / "render" / str(i))
            if not outcome.ok:
                return outcome, f"failed:{outcome.reason}"
            outcomes.append(outcome)
        first = outcomes[0]
        for other in outcomes[1:]:
            if first.png.read_bytes() != other.png.read_bytes():
                return first, "failed:repeat-mismatch"
            if comparable_json(first.json_path) != comparable_json(other.json_path):
                return first, "failed:repeat-mismatch"
        return first, None

    def proposed_record(self, entry: Entry, processed: Any, env: Any) -> dict[str, Any]:
        return {
            "webp_sha256": processed.webp_sha256,
            "pixels_sha256": processed.pixels_sha256,
            "gpgfrontend_commit": self.head,
            "inputs_hash": inputs_hash(entry, self.processing),
            "env_hash": env.env_hash,
            "env": env.lock_env(),
            "generated_at": utc_now_iso(),
        }

    # Per entry -------------------------------------------------------------

    def run_entry(self, entry: Entry, row: Any, selected: bool, accept: set[str], force: set[str]) -> EntryResult:
        res = EntryResult(entry.id, "", {"statuses": list(row.statuses)})
        if ORPHAN in row.statuses:
            res.status = "failed:orphan"
            return res
        if row.details.get("probe_failed"):
            res.status = "failed:env-probe"
            res.details["probe"] = row.details["probe_failed"]
            return res
        if not selected:
            res.status = "unchanged"
            res.details["note"] = "not stale; not rendered"
            return res
        dirty = DIRTY_SOURCES in row.statuses
        if dirty and not self.args.allow_dirty:
            res.status = "refused-dirty"
            res.details["dirty_files"] = row.details.get("dirty_files")
            return res
        preview = "preview-only-dirty" if dirty else (
            "preview-only-platform" if PLATFORM_MISMATCH in row.statuses else None)
        if self.apply and not preview:
            pending = txnmod.pending_for(self.paths, entry.id)
            if pending:
                states = {t.state for t in pending}
                res.status = "upload-unknown" if states & {txnmod.UPLOADING, txnmod.UPLOAD_UNKNOWN} \
                    else "failed:pending-transaction"
                res.details["pending"] = [t.id for t in pending]
                res.details["hint"] = "run run.py --recover first"
                return res
        self.warnings.extend(freshness_warnings(self.renderer.binary, self.args.gpgfrontend,
                                                self.manifest.relevant_sources(entry)))
        outcome, failure = self.render_repeated(entry)
        if failure:
            res.status = failure
            res.details["reason"] = outcome.failure
            return res
        env = outcome.env
        probe = self.renderer.probe(entry)
        if probe.env and probe.env.env_hash != env.env_hash:
            res.status = "failed:probe-render-env-mismatch"
            res.details.update({"probe_env_hash": probe.env.env_hash, "render_env_hash": env.env_hash})
            return res
        if env.platform != entry.platform:
            preview = preview or "preview-only-platform"
        preview_dir = self.cache / "preview"
        try:
            processed = process(outcome.png, outcome.geometry, entry, preview_dir, entry.id)
        except PostprocessError as exc:
            res.status = f"failed:{exc.reason}"
            res.details["reason"] = str(exc)
            return res
        lock_record = read_lock(self.args.lock).get(entry.id)
        result = diffmod.compare(processed.png, self.cache, entry.id, lock_record, entry.diff)
        decision = result.result
        res.details.update({"diff": decision, "diff_detail": result.detail, "platform": env.platform,
                            "env_hash": env.env_hash, "preview": str(processed.png)})
        if entry.id in force:
            decision = diffmod.REPLACE
        elif entry.id in accept and decision == diffmod.BASELINE_UNAVAILABLE:
            decision = diffmod.REPLACE
        elif decision == diffmod.NEW:
            decision = diffmod.REPLACE
        res.details["decision"] = decision
        proposed = self.proposed_record(entry, processed, env)
        atomic_write_json(preview_dir / f"{entry.id}.json", {
            "entry": entry.settings(), "geometry": outcome.geometry, "platform": env.platform,
            "env_hash": env.env_hash, "font_files": env.font_files, "proposed_lock_record": proposed,
            "diff": result.result, "decision": decision,
        })
        if preview:
            res.status = preview
        elif decision == diffmod.BASELINE_UNAVAILABLE:
            res.status = "baseline-unavailable"
        elif decision == diffmod.REPLACE:
            self.replace(entry, res, processed, outcome, proposed)
        else:
            self.unchanged(entry, row, res, lock_record, proposed)
        return res

    def replace(self, entry: Entry, res: EntryResult, processed: Any, outcome: Any,
                proposed: dict[str, Any]) -> None:
        if not self.args.upload:
            res.status = "would-replace"
            return
        if self.stop_txn:
            res.status = "failed:stopped-after-conflict"
            return
        assert self.creds is not None
        try:
            txn = txnmod.prepare(self.paths, entry.id, entry.doc, entry.ref, processed.png, processed.webp,
                                 outcome.geometry, proposed)
        except PipelineError as exc:
            res.status = "failed:prepare"
            res.details["reason"] = str(exc)
            return
        out = txnmod.execute(txn, self.creds)
        res.details.update({"txn": out.txn_id, "txn_state": out.state, "url": out.url})
        if out.detail:
            res.details["reason"] = out.detail
        res.status = {
            txnmod.COMMITTED: "updated",
            txnmod.CONFLICT: "conflict",
            txnmod.UPLOAD_UNKNOWN: "upload-unknown",
            txnmod.ARTIFACT_CORRUPT: "artifact-corrupt",
        }.get(out.state, f"failed:{out.state}")
        if out.state == txnmod.CONFLICT:
            res.del_url = out.del_url
            self.stop_txn = True
        if out.state == txnmod.COMMITTED:
            superseded = superseded_del(self.paths, txn.data["doc"]["old_url"])
            if superseded:
                res.del_url = superseded
                res.details["superseded_url"] = txn.data["doc"]["old_url"]

    def restore_doc_url(self, entry: Entry, row: Any, res: EntryResult,
                        lock_record: Optional[dict[str, Any]]) -> bool:
        """An emptied or TODO link whose image is unchanged gets the locked URL back.

        No upload: the image on the CDN is still the right one. Returns False
        when the entry is not in that state, or it could not be restored.
        """
        if row.details.get("missing") != "empty or TODO url" or not lock_record or not lock_record.get("url"):
            return True
        if not self.apply:
            res.status = "would-restore-doc"
            return False
        path = Path(self.args.manual_root) / entry.doc
        try:
            apply_doc(path, entry.ref, row.details.get("url") or "", lock_record["url"], doc_sha256(path))
        except Conflict as exc:
            res.status = "conflict"
            res.details["reason"] = str(exc)
            return False
        res.details["restored_url"] = lock_record["url"]
        return True

    def unchanged(self, entry: Entry, row: Any, res: EntryResult, lock_record: Optional[dict[str, Any]],
                  proposed: dict[str, Any]) -> None:
        if not self.restore_doc_url(entry, row, res, lock_record):
            return
        restored = "restored_url" in res.details
        if not set(row.statuses) & set(STALE):
            res.status = "unchanged"
            return
        if not self.apply:
            res.status = "unchanged-lock-not-advanced"
            return
        assert lock_record is not None
        target = dict(lock_record)
        for key in ("gpgfrontend_commit", "inputs_hash", "env_hash", "env", "generated_at"):
            target[key] = proposed[key]
        try:
            apply_lock(self.args.lock, entry.id, lock_record, target)
            res.status = "doc-restored" if restored else "lock-advanced"
        except Conflict as exc:
            res.status = "conflict"
            res.details["reason"] = str(exc)


def superseded_del(paths: txnmod.Paths, old_url: str) -> Optional[str]:
    """The del link of an earlier upload of ours that has just been replaced."""
    if not old_url:
        return None
    for t in txnmod.list_txns(paths):
        up = t.data.get("upload") or {}
        if t.state == txnmod.COMMITTED and up.get("url") == old_url and up.get("del"):
            return up["del"]
    return None


def exit_code(results: list[EntryResult], applying: bool) -> int:
    statuses = [r.status for r in results]
    if any(s in PENDING_STATUSES for s in statuses):
        return 3
    bad = [s for s in statuses if s.startswith("failed:") or s in ("refused-dirty", "baseline-unavailable")]
    # A preview-only entry withheld from --apply/--upload counts as refused;
    # in a dry run nothing was withheld.
    if applying:
        bad += [s for s in statuses if s in PREVIEW_STATUSES]
    return 1 if bad else 0


def print_summary(results: list[EntryResult], warnings: list[str]) -> None:
    width = max([len(r.id) for r in results] + [8])
    print("Summary")
    for r in results:
        extra = r.details.get("reason") or r.details.get("diff_detail") or r.details.get("note") or ""
        print(f"  {r.id:<{width}}  {r.status:<28} {extra}".rstrip())
        if r.details.get("url"):
            print(f"  {'':<{width}}  url: {r.details['url']}")
        if r.del_url:
            print(f"  {'':<{width}}  del: {r.del_url}  (delete link, from the local cache only)")
    for w in warnings:
        print(f"warning: {w}")


def write_last_run(cache: Path, argv: list[str], results: list[EntryResult], warnings: list[str],
                   code: int) -> None:
    atomic_write_json(cache / "last-run.json", {
        "generated_at": utc_now_iso(),
        "argv": argv,
        "exit_code": code,
        "warnings": warnings,
        "entries": [r.as_dict() for r in results],
    })


def do_run(args: argparse.Namespace, argv: list[str]) -> int:
    manifest = load_manifest(args.manifest)
    cands = candidates(manifest, args.only)
    binary = args.binary or (Path(os.environ["GF_SCREENSHOT_BINARY"]) if os.environ.get("GF_SCREENSHOT_BINARY") else None)
    if not binary:
        raise UsageError("--binary or GF_SCREENSHOT_BINARY is required to render")
    creds = upload.credentials_from_env() if args.upload else None
    renderer = Renderer(RenderConfig(binary, args.gpgfrontend, args.work_root, args.keep_work))
    # A manifest naming a scenario this binary does not have is a usage error,
    # found before anything is rendered rather than as one failed render.
    known = renderer.list_scenarios()
    unknown = sorted({e.scenario for e in cands if e.scenario} - set(known))
    if unknown:
        raise UsageError(f"scenario(s) not in this binary's --screenshot-list: {', '.join(unknown)}")
    lock = read_lock(args.lock)
    ctx = CheckContext(manifest, lock, args.manual_root, args.gpgfrontend, renderer)
    pages = {p.doc: p for p in docrefs.scan_docs(args.manual_root)}
    rows = {e.id: entry_row(ctx, e, pages) for e in cands}
    selected = {e.id for e in cands if args.force or set(rows[e.id].statuses) & set(STALE)}
    accept, force = validate_overrides(args, selected, lock, args.cache)
    runner = Runner(args, manifest, renderer, creds)
    results = [runner.run_entry(e, rows[e.id], e.id in selected, accept, force) for e in cands]
    warnings = dedupe(runner.warnings)
    code = exit_code(results, runner.apply)
    print_summary(results, warnings)
    write_last_run(args.cache, argv, results, warnings, code)
    return code


def do_recover(args: argparse.Namespace) -> int:
    creds = upload.credentials_from_env() if args.retry_upload else None
    paths = txnmod.Paths(Path(args.manual_root), Path(args.lock), Path(args.cache))
    outcomes = txnmod.recover(paths, args.resolve, args.url, args.retry_upload, creds)
    if not outcomes:
        print("nothing to recover")
        return 0
    for o in outcomes:
        print(f"  {o.txn_id}  {o.entry_id}  {o.state}  {o.detail}".rstrip())
        if o.state in (txnmod.CONFLICT, txnmod.UPLOAD_UNKNOWN, txnmod.UPLOADED) and (o.url or o.del_url):
            print(f"      url: {o.url}  del: {o.del_url}")
        if o.state == txnmod.UPLOAD_UNKNOWN:
            print(f"      decide with: run.py --recover --resolve {o.txn_id} (--url <url> | --retry-upload)")
    states = {o.state for o in outcomes}
    if states & {txnmod.CONFLICT, txnmod.UPLOAD_UNKNOWN, txnmod.ARTIFACT_CORRUPT, txnmod.UPLOADING}:
        return 3
    if txnmod.UPLOAD_FAILED in states:
        return 1
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    args = build_parser().parse_args(argv)
    try:
        validate_flags(args)
        if args.recover:
            return do_recover(args)
        return do_run(args, argv)
    except UsageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except PipelineError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
