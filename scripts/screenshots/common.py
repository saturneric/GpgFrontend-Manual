"""Shared helpers: paths, hashing, canonical JSON and durable file writes."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
MANUAL_ROOT = SCRIPT_DIR.parent.parent
DEFAULT_MANIFEST = SCRIPT_DIR / "screenshots.yaml"
DEFAULT_LOCK = SCRIPT_DIR / "screenshots.lock.json"
DEFAULT_CACHE = SCRIPT_DIR / ".screenshots-cache"
DOCS_SUBDIR = Path("src") / "content" / "docs"

# Windows reports a file held open by another process (an editor, a virus
# scanner) as a sharing violation; os.replace surfaces it as PermissionError.
_REPLACE_ATTEMPTS = 50
_REPLACE_DELAY_S = 0.1


class PipelineError(Exception):
    """An expected failure with a message fit for the user."""


class UsageError(PipelineError):
    """Bad command line or manifest; maps to exit code 2."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(obj: Any) -> bytes:
    """The one serialization every hash in the pipeline is computed over."""
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_stamp_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def fsync_dir(path: Path) -> None:
    """Persist a directory entry change. Not possible (or needed) on Windows."""
    if os.name == "nt":
        return
    fd = os.open(str(path), os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _is_sharing_violation(exc: OSError) -> bool:
    if os.name != "nt":
        return False
    winerror = getattr(exc, "winerror", None)
    return isinstance(exc, PermissionError) or winerror in (5, 32, 33)


def replace_with_retry(src: Path, dst: Path) -> None:
    for attempt in range(_REPLACE_ATTEMPTS):
        try:
            os.replace(str(src), str(dst))
            return
        except OSError as exc:
            if not _is_sharing_violation(exc) or attempt == _REPLACE_ATTEMPTS - 1:
                raise
            time.sleep(_REPLACE_DELAY_S)


def atomic_write_bytes(path: Path, data: bytes) -> None:
    """Temp file in the same directory, flush, fsync, os.replace, dir fsync."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        replace_with_retry(tmp, path)
        fsync_dir(path.parent)
    except BaseException:
        try:
            tmp.unlink()
        except OSError:
            pass
        raise


def atomic_write_text(path: Path, text: str) -> None:
    """Writes text exactly as given: no newline translation, UTF-8."""
    atomic_write_bytes(path, text.encode("utf-8"))


def dump_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def atomic_write_json(path: Path, obj: Any) -> None:
    atomic_write_text(path, dump_json(obj))


def atomic_copy(src: Path, dst: Path) -> None:
    atomic_write_bytes(dst, Path(src).read_bytes())


def append_line_durable(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line.rstrip("\n") + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def read_text_exact(path: Path) -> str:
    """Reads UTF-8 without newline translation, so CRLF survives a rewrite."""
    return Path(path).read_bytes().decode("utf-8")


def load_json(path: Path, default: Any = None) -> Any:
    path = Path(path)
    if not path.exists():
        return default
    try:
        return json.loads(read_text_exact(path))
    except json.JSONDecodeError as exc:
        raise PipelineError(f"{path}: invalid JSON: {exc}") from exc


def split_ids(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def is_missing_error(exc: OSError) -> bool:
    return exc.errno == errno.ENOENT
