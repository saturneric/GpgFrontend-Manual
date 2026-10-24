"""Local writes: the doc definition URL and the lock record.

Both are idempotent and refuse to overwrite anything they did not expect,
raising Conflict instead.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import docrefs
from common import PipelineError, atomic_write_json, atomic_write_text, load_json, read_text_exact, sha256_bytes

LOCK_FIELDS = ("url", "webp_sha256", "pixels_sha256", "gpgfrontend_commit",
               "inputs_hash", "env_hash", "env", "generated_at")
WRITTEN = "written"
ALREADY = "already-applied"


class Conflict(PipelineError):
    pass


def _contains_del(obj: Any) -> bool:
    if isinstance(obj, dict):
        return "del" in obj or any(_contains_del(v) for v in obj.values())
    if isinstance(obj, list):
        return any(_contains_del(v) for v in obj)
    return False


def read_lock(path: Path) -> dict[str, Any]:
    data = load_json(path, {})
    if not isinstance(data, dict):
        raise PipelineError(f"{path}: the lock must be a JSON object keyed by entry id")
    return data


def write_lock(path: Path, lock: dict[str, Any]) -> None:
    if _contains_del(lock):
        raise PipelineError("refusing to write a `del` capability URL into the committed lock")
    atomic_write_json(path, lock)


def doc_sha256(path: Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def apply_doc(path: Path, label: str, old_url: str, new_url: str, sha_before: str) -> str:
    """Points the single definition of `label` at new_url.

    Unchanged doc: rewrite it. Concurrently edited doc: rewrite only if the
    definition still carries old_url. Already new_url: nothing to do.
    """
    path = Path(path)
    if not path.is_file():
        raise Conflict(f"{path} no longer exists")
    text = read_text_exact(path)
    if sha256_bytes(text.encode("utf-8")) == sha_before:
        atomic_write_text(path, docrefs.replace_definition_url(text, label, new_url, old_url))
        return WRITTEN
    defs = docrefs.find_definitions(text, label)
    if len(defs) != 1:
        raise Conflict(f"{path}: [{label}] now has {len(defs)} definitions")
    if defs[0].url == new_url:
        return ALREADY
    if defs[0].url != old_url:
        raise Conflict(f"{path}: [{label}] was changed to {defs[0].url!r}")
    atomic_write_text(path, docrefs.replace_url(text, defs[0], new_url))
    return WRITTEN


def lock_state(path: Path, entry_id: str, before: Optional[dict[str, Any]],
               target: dict[str, Any]) -> str:
    current = read_lock(path).get(entry_id)
    if current == target:
        return "target"
    if current == before:
        return "before"
    return "other"


def apply_lock(path: Path, entry_id: str, before: Optional[dict[str, Any]], target: dict[str, Any]) -> str:
    lock = read_lock(path)
    current = lock.get(entry_id)
    if current == target:
        return ALREADY
    if current != before:
        raise Conflict(f"lock record for {entry_id} was changed by something else")
    lock[entry_id] = target
    write_lock(path, lock)
    return WRITTEN
