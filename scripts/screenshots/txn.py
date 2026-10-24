"""Durable upload/apply transaction, one per replaced image.

States: prepared -> uploading -> uploaded -> doc-applied -> lock-applied
-> committed, with the terminal side exits abandoned, upload-failed,
conflict and artifact-corrupt, and upload-unknown, which waits for a
decision (`run.py --recover --resolve`).

Every state is persisted to txn.json (temp file, fsync, os.replace, dir
fsync) before the step that depends on it. Recovery reads only txn.json;
journal.jsonl is an audit log.
"""

from __future__ import annotations

import json
import os
import secrets
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

import docrefs
import upload
from apply import Conflict, apply_doc, apply_lock, doc_sha256, lock_state, read_lock
from common import (PipelineError, UsageError, append_line_durable, atomic_copy, atomic_write_json,
                    load_json, read_text_exact, sha256_file, utc_now_iso, utc_stamp_compact)

SCHEMA = 1
PREPARED = "prepared"
UPLOADING = "uploading"
UPLOADED = "uploaded"
DOC_APPLIED = "doc-applied"
LOCK_APPLIED = "lock-applied"
COMMITTED = "committed"
ABANDONED = "abandoned"
UPLOAD_FAILED = "upload-failed"
UPLOAD_UNKNOWN = "upload-unknown"
CONFLICT = "conflict"
ARTIFACT_CORRUPT = "artifact-corrupt"

TERMINAL = (COMMITTED, ABANDONED, UPLOAD_FAILED, CONFLICT, ARTIFACT_CORRUPT)
DEL_UNKNOWN = "unknown"

# Test hook: raise InjectedCrash right after this state has been persisted.
CRASH_ENV = "GF_SHOTS_TEST_CRASH_AFTER"
crash_hook: Optional[Callable[[str], None]] = None

_PLACEHOLDER_URL = "https://placeholder.invalid/prepare-check.webp"

Uploader = Callable[[upload.Credentials, Path, str], upload.Uploaded]


class InjectedCrash(BaseException):
    """Simulates the process dying; BaseException so nothing swallows it."""


@dataclass
class Paths:
    manual_root: Path
    lock: Path
    cache: Path

    @property
    def txn_root(self) -> Path:
        return self.cache / "txn"

    @property
    def journal(self) -> Path:
        return self.txn_root / "journal.jsonl"

    def baseline(self, entry_id: str) -> Path:
        return self.cache / "baseline" / f"{entry_id}.png"


@dataclass
class Outcome:
    txn_id: str
    entry_id: str
    state: str
    detail: str = ""
    url: Optional[str] = None
    del_url: Optional[str] = None


class Txn:
    def __init__(self, directory: Path, data: dict[str, Any], paths: Paths) -> None:
        self.dir = directory
        self.data = data
        self.paths = paths

    @property
    def id(self) -> str:
        return self.data["txn_id"]

    @property
    def entry_id(self) -> str:
        return self.data["entry_id"]

    @property
    def state(self) -> str:
        return self.data["state"]

    @classmethod
    def load(cls, directory: Path, paths: Paths) -> "Txn":
        data = load_json(directory / "txn.json")
        if not isinstance(data, dict) or data.get("schema") != SCHEMA:
            raise PipelineError(f"{directory}: unreadable txn.json")
        return cls(directory, data, paths)

    def persist(self, state: str, detail: str = "") -> None:
        at = utc_now_iso()
        self.data["state"] = state
        self.data.setdefault("state_history", []).append({"state": state, "at": at})
        self.data["detail"] = detail
        atomic_write_json(self.dir / "txn.json", self.data)
        append_line_durable(self.paths.journal, json.dumps(
            {"txn_id": self.id, "entry_id": self.entry_id, "state": state, "at": at}, sort_keys=True))
        if os.environ.get(CRASH_ENV) == state:
            raise InjectedCrash(state)
        if crash_hook is not None:
            crash_hook(state)

    def outcome(self) -> Outcome:
        up = self.data.get("upload") or {}
        return Outcome(self.id, self.entry_id, self.state, self.data.get("detail", ""),
                       up.get("url"), up.get("del"))

    def artifacts_intact(self) -> bool:
        arts = self.data["artifacts"]
        for kind in ("png", "webp"):
            path = self.dir / arts[kind]["file"]
            if not path.is_file() or sha256_file(path) != arts[kind]["sha256"]:
                return False
        return True

    def target_record(self) -> dict[str, Any]:
        record = dict(self.data["proposed_lock_record"])
        record["url"] = self.data["upload"]["url"]
        return record


def prepare(paths: Paths, entry_id: str, doc_rel: str, ref: str, final_png: Path, final_webp: Path,
            render_record: dict[str, Any], proposed: dict[str, Any]) -> Txn:
    """Validates everything that can be checked offline. On failure no
    transaction exists and nothing has been uploaded."""
    if "url" in proposed:
        raise PipelineError("proposed lock record must not carry a url")
    doc_path = paths.manual_root / doc_rel
    if not doc_path.is_file():
        raise PipelineError(f"doc not found: {doc_rel}")
    text = read_text_exact(doc_path)
    defs = docrefs.find_definitions(text, ref)
    if len(defs) != 1:
        raise PipelineError(f"{doc_rel}: [{ref}] has {len(defs)} definitions, expected exactly one")
    definition = defs[0]
    rewritten = docrefs.replace_url(text, definition, _PLACEHOLDER_URL)
    check = docrefs.find_definitions(rewritten, ref)
    if len(check) != 1 or check[0].url != _PLACEHOLDER_URL:
        raise PipelineError(f"{doc_rel}: cannot rewrite [{ref}] safely")

    txn_id = f"{utc_stamp_compact()}-{entry_id}-{secrets.token_hex(4)}"
    directory = paths.txn_root / txn_id
    directory.mkdir(parents=True)
    try:
        atomic_copy(final_png, directory / "final.png")
        atomic_copy(final_webp, directory / "final.webp")
        atomic_write_json(directory / "render.json", render_record)
        webp_size = (directory / "final.webp").stat().st_size
        data = {
            "schema": SCHEMA,
            "txn_id": txn_id,
            "entry_id": entry_id,
            "state": None,
            "state_history": [],
            "artifacts": {
                "png": {"file": "final.png", "sha256": sha256_file(directory / "final.png")},
                "webp": {"file": "final.webp", "sha256": sha256_file(directory / "final.webp"),
                         "bytes": webp_size},
            },
            "proposed_lock_record": proposed,
            "lock_record_before": read_lock(paths.lock).get(entry_id),
            "doc": {
                "path": doc_rel,
                "ref": ref,
                "old_url": definition.url,
                "sha256_before": doc_sha256(doc_path),
                "definition": {
                    "line_start": definition.line_start,
                    "line_end": definition.line_end,
                    "text_before": definition.text,
                },
            },
            "upload": None,
        }
        if data["artifacts"]["webp"]["sha256"] != proposed.get("webp_sha256"):
            raise PipelineError("final.webp does not match the proposed lock record")
        txn = Txn(directory, data, paths)
    except BaseException:
        shutil.rmtree(directory, ignore_errors=True)
        raise
    txn.persist(PREPARED)
    return txn


def _lock_precheck(txn: Txn) -> None:
    state = lock_state(txn.paths.lock, txn.entry_id, txn.data["lock_record_before"], _maybe_target(txn))
    if state == "other":
        raise Conflict(f"lock record for {txn.entry_id} changed since the transaction was prepared")


def _maybe_target(txn: Txn) -> dict[str, Any]:
    if txn.data.get("upload") and txn.data["upload"].get("url"):
        return txn.target_record()
    return {"__no_target__": True}


def _do_upload(txn: Txn, creds: upload.Credentials, uploader: Uploader) -> None:
    txn.data["upload"] = {"endpoint_host": creds.host, "attempted_at": utc_now_iso(),
                          "response_raw": None, "url": None, "del": None}
    txn.persist(UPLOADING)
    try:
        result = uploader(creds, txn.dir / "final.webp", f"{txn.entry_id}.webp")
    except upload.UploadFailed as exc:
        txn.data["upload"]["response_raw"] = exc.raw
        txn.persist(UPLOAD_FAILED, exc.reason)
        return
    except upload.UploadUnknown as exc:
        txn.persist(UPLOAD_UNKNOWN, f"no response after sending: {exc}")
        return
    txn.data["upload"].update({"response_raw": result.raw, "url": result.url, "del": result.del_url})
    txn.persist(UPLOADED)


def _advance(txn: Txn) -> None:
    """Runs the local steps from the current state to committed."""
    try:
        while txn.state not in TERMINAL and txn.state != UPLOAD_UNKNOWN:
            if txn.state == UPLOADED:
                _lock_precheck(txn)
                doc = txn.data["doc"]
                apply_doc(txn.paths.manual_root / doc["path"], doc["ref"], doc["old_url"],
                          txn.data["upload"]["url"], doc["sha256_before"])
                txn.persist(DOC_APPLIED)
            elif txn.state == DOC_APPLIED:
                apply_lock(txn.paths.lock, txn.entry_id, txn.data["lock_record_before"], txn.target_record())
                txn.persist(LOCK_APPLIED)
            elif txn.state == LOCK_APPLIED:
                baseline = txn.paths.baseline(txn.entry_id)
                atomic_copy(txn.dir / "final.png", baseline)
                if sha256_file(baseline) != txn.data["artifacts"]["png"]["sha256"]:
                    raise PipelineError(f"baseline copy for {txn.entry_id} does not match final.png")
                txn.persist(COMMITTED)
            else:
                raise PipelineError(f"cannot advance a transaction in state {txn.state}")
    except Conflict as exc:
        txn.persist(CONFLICT, str(exc))


def execute(txn: Txn, creds: upload.Credentials, uploader: Uploader = upload.upload_file) -> Outcome:
    if txn.state != PREPARED:
        raise PipelineError(f"{txn.id} is not prepared")
    if not txn.artifacts_intact():
        txn.persist(ARTIFACT_CORRUPT, "artifacts changed before upload")
        return txn.outcome()
    try:
        _lock_precheck(txn)
    except Conflict as exc:
        txn.persist(CONFLICT, str(exc))
        return txn.outcome()
    _do_upload(txn, creds, uploader)
    _advance(txn)
    return txn.outcome()


def list_txns(paths: Paths) -> list[Txn]:
    if not paths.txn_root.is_dir():
        return []
    out = []
    for directory in sorted(p for p in paths.txn_root.iterdir() if p.is_dir()):
        if (directory / "txn.json").is_file():
            out.append(Txn.load(directory, paths))
    return out


def pending_for(paths: Paths, entry_id: str) -> list[Txn]:
    """Transactions for an entry that still need --recover."""
    return [t for t in list_txns(paths) if t.entry_id == entry_id and t.state not in TERMINAL]


def recover(paths: Paths, resolve: Optional[str] = None, url: Optional[str] = None,
            retry_upload: bool = False, creds: Optional[upload.Credentials] = None,
            uploader: Uploader = upload.upload_file) -> list[Outcome]:
    """Completes every non-terminal transaction without rendering.

    Only an explicit --resolve moves an upload-unknown transaction on.
    """
    txns = list_txns(paths)
    if resolve is not None:
        match = [t for t in txns if t.id == resolve]
        if not match:
            raise UsageError(f"no transaction {resolve}")
        if match[0].state not in (UPLOADING, UPLOAD_UNKNOWN):
            raise UsageError(f"{resolve} is {match[0].state}; only upload-unknown can be resolved")
        if bool(url) == bool(retry_upload):
            raise UsageError("--resolve needs exactly one of --url or --retry-upload")
        if url and not upload.is_https_url(url):
            raise UsageError(f"--url must be an https URL, got {url!r}")
        if retry_upload and creds is None:
            raise UsageError("--retry-upload needs CDN credentials")
    outcomes: list[Outcome] = []
    stopped = False
    for txn in txns:
        if txn.state in TERMINAL:
            continue
        if stopped:
            outcomes.append(Outcome(txn.id, txn.entry_id, txn.state, "not processed: an earlier conflict stopped the run"))
            continue
        if not txn.artifacts_intact():
            txn.persist(ARTIFACT_CORRUPT, "final.png or final.webp does not match txn.json")
        elif txn.state == PREPARED:
            txn.persist(ABANDONED, "nothing was uploaded")
        else:
            if txn.state == UPLOADING:
                txn.persist(UPLOAD_UNKNOWN, "interrupted after the request may have been sent")
            if txn.state == UPLOAD_UNKNOWN and txn.id == resolve:
                if url:
                    txn.data["upload"].update({"url": url, "del": DEL_UNKNOWN,
                                               "response_raw": "resolved by hand"})
                    txn.persist(UPLOADED, "url supplied with --resolve; del unknown")
                else:
                    assert creds is not None
                    _do_upload(txn, creds, uploader)
            _advance(txn)
        outcomes.append(txn.outcome())
        if txn.state == CONFLICT:
            stopped = True
    return outcomes
