"""Reports the status of every managed entry and every image ref in the manual.

usage: check.py --gpgfrontend <repo> [--binary <exe>] [--inventory] [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import docrefs
import gitutil
from apply import read_lock
from common import (DEFAULT_LOCK, DEFAULT_MANIFEST, MANUAL_ROOT, SCRIPT_DIR, PipelineError, UsageError)
from manifest import Entry, Manifest, inputs_hash, load_manifest
from postprocess import processing_descriptor
from render import RenderConfig, Renderer

MISSING = "missing"
UNMANAGED = "unmanaged"
ORPHAN = "orphan"
UNKNOWN_BASELINE = "unknown-baseline"
OUTDATED = "outdated"
INPUTS_CHANGED = "inputs-changed"
ENV_CHANGED = "env-changed"
ENV_UNCHECKED = "env-unchecked"
DIRTY_SOURCES = "dirty-sources"
PLATFORM_MISMATCH = "platform-mismatch"
OK = "ok"

STALE = (MISSING, UNKNOWN_BASELINE, OUTDATED, INPUTS_CHANGED, ENV_CHANGED)
STATUS_ORDER = (MISSING, UNMANAGED, ORPHAN, UNKNOWN_BASELINE, OUTDATED, INPUTS_CHANGED, ENV_CHANGED,
                ENV_UNCHECKED, DIRTY_SOURCES, PLATFORM_MISMATCH, "manual-only", "animated", OK)


@dataclass
class Row:
    id: Optional[str]
    doc: str
    ref: Optional[str]
    statuses: list[str]
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "doc": self.doc, "ref": self.ref,
                "statuses": list(self.statuses), "details": self.details}


@dataclass
class CheckContext:
    manifest: Manifest
    lock: dict[str, Any]
    manual_root: Path
    gpgfrontend: Path
    renderer: Optional[Renderer] = None
    pipeline_dir: Path = SCRIPT_DIR
    processing: Optional[dict[str, str]] = None

    def processing_info(self) -> dict[str, str]:
        if self.processing is None:
            self.processing = processing_descriptor()
        return self.processing


def _page_map(pages: list[docrefs.PageScan]) -> dict[str, docrefs.PageScan]:
    return {page.doc: page for page in pages}


def _baseline_statuses(ctx: CheckContext, entry: Entry, record: dict[str, Any], row: Row) -> None:
    commit = str(record.get("gpgfrontend_commit") or "")
    row.details["lock_commit"] = commit or None
    if not gitutil.commit_exists(ctx.gpgfrontend, commit):
        row.statuses.append(UNKNOWN_BASELINE)
        row.details["baseline"] = "lock commit not found in the GpgFrontend repository"
        return
    if not gitutil.is_ancestor(ctx.gpgfrontend, commit):
        row.statuses.append(UNKNOWN_BASELINE)
        row.details["baseline"] = "lock commit is not an ancestor of HEAD"
        return
    changed = gitutil.changed_since(ctx.gpgfrontend, commit, ctx.manifest.relevant_sources(entry))
    if changed:
        row.statuses.append(OUTDATED)
        row.details["changed_files"] = changed


def _env_statuses(ctx: CheckContext, entry: Entry, record: Optional[dict[str, Any]], row: Row) -> None:
    if ctx.renderer is None:
        row.statuses.append(ENV_UNCHECKED)
        return
    probe = ctx.renderer.probe(entry)
    if not probe.ok or probe.env is None:
        row.statuses.append(ENV_UNCHECKED)
        row.details["probe_failed"] = probe.failure
        return
    row.details["platform"] = probe.env.platform
    row.details["env_hash"] = probe.env.env_hash
    if record and record.get("env_hash") != probe.env.env_hash:
        row.statuses.append(ENV_CHANGED)
        row.details["lock_env_hash"] = record.get("env_hash")
    if probe.env.platform != entry.platform:
        row.statuses.append(PLATFORM_MISMATCH)


def entry_row(ctx: CheckContext, entry: Entry, pages: dict[str, docrefs.PageScan]) -> Row:
    row = Row(entry.id, entry.doc, entry.ref, [])
    page = pages.get(entry.doc)
    if page is None or not page.has_reference(entry.ref):
        row.statuses.append(ORPHAN)
    else:
        definition = page.definition_for(entry.ref)
        url = definition.url if definition else None
        row.details["url"] = url
        if docrefs.is_missing_url(url):
            row.statuses.append(MISSING)
            row.details["missing"] = "no definition" if definition is None else "empty or TODO url"
        if len(page.definitions.get(docrefs.normalize_label(entry.ref), [])) > 1:
            row.details["duplicate_definitions"] = True
    if not entry.renderable:
        row.statuses.append(entry.status or "")
        return row
    record = ctx.lock.get(entry.id)
    if not record:
        if MISSING not in row.statuses:
            row.statuses.append(MISSING)
        row.details.setdefault("missing", "no lock record")
    else:
        _baseline_statuses(ctx, entry, record, row)
        current = inputs_hash(entry, ctx.processing_info(), ctx.pipeline_dir)
        if record.get("inputs_hash") != current:
            row.statuses.append(INPUTS_CHANGED)
    _env_statuses(ctx, entry, record, row)
    dirty = gitutil.dirty(ctx.gpgfrontend, ctx.manifest.relevant_sources(entry))
    if dirty:
        row.statuses.append(DIRTY_SOURCES)
        row.details["dirty_files"] = dirty
    if not row.statuses:
        row.statuses.append(OK)
    return row


def unmanaged_rows(ctx: CheckContext, pages: list[docrefs.PageScan]) -> list[Row]:
    managed = {(e.doc, docrefs.normalize_label(e.ref)) for e in ctx.manifest.entries}
    rows: list[Row] = []
    for page in pages:
        seen: set[tuple[str, str]] = set()
        for ref in page.refs:
            if ref.kind == "reference":
                key = (page.doc, ref.label or "")
                if key in managed or key in seen:
                    continue
                seen.add(key)
                url = page.ref_url(ref)
                statuses = [UNMANAGED] + ([MISSING] if docrefs.is_missing_url(url) else [])
                rows.append(Row(None, page.doc, ref.raw_label, statuses,
                                {"url": url, "line": ref.line, "kind": ref.kind}))
            else:
                rows.append(Row(None, page.doc, None, [UNMANAGED],
                                {"url": ref.url, "line": ref.line, "kind": ref.kind}))
    return rows


def compute(ctx: CheckContext) -> tuple[list[Row], list[docrefs.PageScan]]:
    gitutil.head(ctx.gpgfrontend)
    pages = docrefs.scan_docs(ctx.manual_root)
    page_map = _page_map(pages)
    rows = [entry_row(ctx, entry, page_map) for entry in ctx.manifest.entries]
    rows.extend(unmanaged_rows(ctx, pages))
    return rows, pages


def managed_map(manifest: Manifest) -> dict[tuple[str, str], str]:
    return {(e.doc, docrefs.normalize_label(e.ref)): e.id for e in manifest.entries}


def _short(row: Row) -> str:
    d = row.details
    bits = []
    for key in ("missing", "baseline", "probe_failed", "kind"):
        if d.get(key):
            bits.append(f"{key}={d[key]}")
    if d.get("changed_files"):
        bits.append(f"changed={len(d['changed_files'])} file(s)")
    if d.get("dirty_files"):
        bits.append(f"dirty={len(d['dirty_files'])} file(s)")
    if d.get("platform"):
        bits.append(f"platform={d['platform']}")
    if d.get("line"):
        bits.append(f"line {d['line']}")
    return "  ".join(bits)


def format_table(rows: list[Row]) -> str:
    lines: list[str] = []
    for status in STATUS_ORDER:
        group = [r for r in rows if status in r.statuses]
        if not group:
            continue
        lines.append(f"{status} ({len(group)})")
        for r in group:
            ident = r.id or "-"
            ref = f"[{r.ref}]" if r.ref else ""
            lines.append(f"  {ident:<28} {r.doc} {ref}  {_short(r)}".rstrip())
        lines.append("")
    return "\n".join(lines)


def _fmt_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{k}={v}" for k, v in counts.items()) or "-"


def format_inventory(inv: dict[str, Any]) -> str:
    t = inv["total"]
    lines = [
        "Inventory (observed; formats by URL extension, content not fetched)",
        f"  pages with images: {t['pages_with_images']}",
        f"  references:        {t['references']}",
        f"  definitions:       {t['definitions']}",
        f"  unique URLs:       {t['unique_urls']}",
        f"  formats by reference:  {_fmt_counts(t['formats_by_reference'])}",
        f"  formats by unique URL: {_fmt_counts(t['formats_by_unique_url'])}",
        "",
        "Per page (refs / defs / unique URLs / formats by reference)",
    ]
    for p in inv["pages"]:
        lines.append(f"  {p['doc']:<56} {p['references']:>3} {p['definitions']:>3} {p['unique_urls']:>3}  "
                     f"{_fmt_counts(p['formats_by_reference'])}")
    lines.append("")
    managed = sum(1 for r in inv["refs"] if r["managed_id"])
    lines.append(f"Refs ({len(inv['refs'])}; managed {managed}, unmanaged {len(inv['refs']) - managed})")
    for r in inv["refs"]:
        label = f"[{r['ref']}]" if r["ref"] else f"({r['kind']})"
        who = r["managed_id"] or "unmanaged"
        lines.append(f"  {r['doc']}:{r['line']:<4} {label:<10} {r['format']:<5} {who:<28} {r['url'] or '-'}")
    return "\n".join(lines)


def build_context(args: argparse.Namespace) -> CheckContext:
    manifest = load_manifest(args.manifest)
    renderer = None
    binary = args.binary or os.environ.get("GF_SCREENSHOT_BINARY")
    if binary:
        renderer = Renderer(RenderConfig(Path(binary), args.gpgfrontend, args.work_root))
    return CheckContext(manifest, read_lock(args.lock), args.manual_root, args.gpgfrontend, renderer)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Status of manual screenshots.")
    parser.add_argument("--gpgfrontend", required=True, type=Path, help="GpgFrontend repository")
    parser.add_argument("--binary", type=Path, help="screenshot-mode binary (else $GF_SCREENSHOT_BINARY)")
    parser.add_argument("--inventory", action="store_true", help="also report image counts")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--manual-root", type=Path, default=MANUAL_ROOT)
    parser.add_argument("--work-root", type=Path, help="throwaway directory root for probes")
    args = parser.parse_args(argv)
    try:
        ctx = build_context(args)
        rows, pages = compute(ctx)
    except UsageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except PipelineError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    inv = docrefs.inventory(pages, managed_map(ctx.manifest)) if args.inventory else None
    if args.json:
        payload: Any = [r.as_dict() for r in rows]
        if inv is not None:
            payload = {"entries": payload, "inventory": inv}
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    if ctx.renderer is None:
        print("note: no --binary or GF_SCREENSHOT_BINARY; the environment was not probed (env-unchecked)\n")
    print(format_table(rows))
    if inv is not None:
        print(format_inventory(inv))
    return 0


if __name__ == "__main__":
    sys.exit(main())
