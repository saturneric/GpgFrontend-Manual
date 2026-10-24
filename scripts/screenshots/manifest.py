"""Loads screenshots.yaml and resolves every entry against the defaults.

check.py, render.py and run.py all go through resolve(), so the
configuration that is probed, rendered and hashed is always the same one.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from common import SCRIPT_DIR, UsageError, canonical_json, read_text_exact, sha256_bytes, sha256_file

KNOWN_PLATFORMS = ("windows11", "linux-xvfb")
ENTRY_STATUSES = ("manual-only", "animated")
HIGHLIGHT_STYLES = ("box", "arrow")
THEMES = ("light", "dark")

_SIZE_RE = re.compile(r"^([1-9][0-9]{1,4})x([1-9][0-9]{1,4})$")
_CLOCK_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

BUILTIN_DEFAULTS: dict[str, Any] = {
    "platform": "windows11",
    "locale": "en_US",
    "theme": "light",
    "size": "1280x960",
    "fonts": ["Noto Sans", "Noto Sans CJK SC"],
    "clock": "2026-01-15T10:00:00Z",
    "timeout_ms": 30000,
    "frame": {"radius": 8, "shadow": 12, "padding": 24},
    "diff": {"tolerance": 16, "threshold": 0.001},
    "preview_platforms": ["linux-xvfb"],
}

_ENTRY_KEYS = {
    "id", "doc", "ref", "scenario", "locale", "platform", "size", "theme",
    "fonts", "clock", "timeout_ms", "sources", "highlight", "crop", "status",
    "frame", "diff",
}
_DEFAULT_KEYS = set(BUILTIN_DEFAULTS)
_FRAME_KEYS = {"radius", "shadow", "padding"}
_DIFF_KEYS = {"tolerance", "threshold"}

# Settings that never change pixels; they stay out of inputs_hash so that
# moving an image to another page does not force a re-render.
_NON_RENDER_KEYS = ("id", "doc", "ref", "sources", "status", "timeout_ms")


@dataclass(frozen=True)
class Highlight:
    name: str
    style: str = "box"

    def as_dict(self) -> dict[str, str]:
        return {"name": self.name, "style": self.style}


@dataclass(frozen=True)
class Entry:
    id: str
    doc: str
    ref: str
    scenario: str | None
    locale: str
    platform: str
    size: tuple[int, int] | None  # None means "auto": the scenario's natural size
    theme: str
    fonts: tuple[str, ...]
    clock: str
    timeout_ms: int
    sources: tuple[str, ...]
    highlight: tuple[Highlight, ...]
    crop: str | None  # a named widget the image is cut down to, or the whole capture
    status: str | None
    frame: dict[str, Any] = field(hash=False, compare=False)
    diff: dict[str, Any] = field(hash=False, compare=False)

    @property
    def renderable(self) -> bool:
        return self.status is None

    @property
    def size_str(self) -> str:
        return "auto" if self.size is None else f"{self.size[0]}x{self.size[1]}"

    def probe_key(self) -> tuple[str, str, tuple[str, ...], str, tuple[int, int] | None]:
        return (self.locale, self.theme, self.fonts, self.clock, self.size)

    def settings(self) -> dict[str, Any]:
        """The fully resolved entry as plain JSON data."""
        return {
            "id": self.id,
            "doc": self.doc,
            "ref": self.ref,
            "scenario": self.scenario,
            "locale": self.locale,
            "platform": self.platform,
            "size": self.size_str,
            "theme": self.theme,
            "fonts": list(self.fonts),
            "clock": self.clock,
            "timeout_ms": self.timeout_ms,
            "sources": list(self.sources),
            "highlight": [h.as_dict() for h in self.highlight],
            "crop": self.crop,
            "status": self.status,
            "frame": dict(self.frame),
            "diff": dict(self.diff),
        }


@dataclass
class Manifest:
    path: Path
    defaults: dict[str, Any]
    global_sources: tuple[str, ...]
    preview_platforms: tuple[str, ...]
    entries: list[Entry]

    def by_id(self) -> dict[str, Entry]:
        return {entry.id: entry for entry in self.entries}

    def relevant_sources(self, entry: Entry) -> list[str]:
        return list(entry.sources) + [s for s in self.global_sources if s not in entry.sources]


def _fail(where: str, message: str) -> UsageError:
    return UsageError(f"screenshots.yaml: {where}: {message}")


def _check_keys(where: str, data: dict[str, Any], allowed: set[str]) -> None:
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise _fail(where, f"unknown key(s): {', '.join(unknown)}")


def parse_size(where: str, value: Any) -> tuple[int, int] | None:
    if str(value) == "auto":
        return None
    match = _SIZE_RE.match(str(value))
    if not match:
        raise _fail(where, f"size must look like 1100x680 or be auto, got {value!r}")
    return int(match.group(1)), int(match.group(2))


def validate_clock(where: str, value: Any) -> str:
    text = str(value)
    if not _CLOCK_RE.match(text):
        raise _fail(where, f"clock must be ISO-8601 UTC like 2026-01-15T10:00:00Z, got {value!r}")
    try:
        datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise _fail(where, f"clock {text!r} is not a real date: {exc}") from exc
    return text


def _fonts(where: str, value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        value = [v.strip() for v in value.split(",")]
    if not isinstance(value, list) or not value:
        raise _fail(where, "fonts must be a non-empty list of family names")
    out = []
    for family in value:
        if not isinstance(family, str) or not family.strip() or "," in family:
            raise _fail(where, f"invalid font family {family!r}")
        out.append(family.strip())
    return tuple(out)


def _merge_section(where: str, base: dict[str, Any], override: Any, keys: set[str]) -> dict[str, Any]:
    if override is None:
        return dict(base)
    if not isinstance(override, dict):
        raise _fail(where, "must be a mapping")
    _check_keys(where, override, keys)
    merged = dict(base)
    merged.update(override)
    return merged


def _highlights(where: str, value: Any) -> tuple[Highlight, ...]:
    if value is None:
        return ()
    items = value if isinstance(value, list) else [value]
    out: list[Highlight] = []
    for item in items:
        if isinstance(item, str):
            out.append(Highlight(item))
            continue
        if not isinstance(item, dict) or "name" not in item:
            raise _fail(where, f"highlight must be a name or {{name, style}}, got {item!r}")
        _check_keys(where + ".highlight", item, {"name", "style"})
        style = item.get("style", "box")
        if style not in HIGHLIGHT_STYLES:
            raise _fail(where, f"highlight style must be box or arrow, got {style!r}")
        out.append(Highlight(str(item["name"]), style))
    return tuple(out)


def _str_list(where: str, value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
        raise _fail(where, "must be a list of non-empty strings")
    return tuple(value)


def _resolve_entry(index: int, raw: Any, defaults: dict[str, Any]) -> Entry:
    where = f"entries[{index}]"
    if not isinstance(raw, dict):
        raise _fail(where, "must be a mapping")
    _check_keys(where, raw, _ENTRY_KEYS)
    entry_id = raw.get("id")
    if not isinstance(entry_id, str) or not _ID_RE.match(entry_id):
        raise _fail(where, f"id must be lower-case letters, digits and dashes, got {entry_id!r}")
    where = f"entry {entry_id}"
    for key in ("doc", "ref"):
        if not isinstance(raw.get(key), str) or not raw[key].strip():
            raise _fail(where, f"{key} is required")
    status = raw.get("status")
    if status is not None and status not in ENTRY_STATUSES:
        raise _fail(where, f"status must be one of {', '.join(ENTRY_STATUSES)}")
    scenario = raw.get("scenario")
    if status is None and (not isinstance(scenario, str) or not scenario):
        raise _fail(where, "scenario is required unless status is manual-only or animated")

    def pick(key: str) -> Any:
        return raw[key] if key in raw else defaults[key]

    platform = str(pick("platform"))
    if platform not in KNOWN_PLATFORMS:
        raise _fail(where, f"platform must be one of {', '.join(KNOWN_PLATFORMS)}")
    theme = str(pick("theme"))
    if theme not in THEMES:
        raise _fail(where, "theme must be light or dark")
    timeout_ms = pick("timeout_ms")
    if not isinstance(timeout_ms, int) or timeout_ms <= 0:
        raise _fail(where, "timeout_ms must be a positive integer")
    doc = raw["doc"].replace("\\", "/").strip()
    crop = raw.get("crop")
    if crop is not None and (not isinstance(crop, str) or not crop.strip()):
        raise _fail(where, f"crop must be a widget name, got {crop!r}")
    return Entry(
        id=entry_id,
        doc=doc,
        ref=raw["ref"].strip(),
        scenario=scenario if isinstance(scenario, str) else None,
        locale=str(pick("locale")),
        platform=platform,
        size=parse_size(where, pick("size")),
        theme=theme,
        fonts=_fonts(where, pick("fonts")),
        clock=validate_clock(where, pick("clock")),
        timeout_ms=timeout_ms,
        sources=_str_list(where + ".sources", raw.get("sources")),
        highlight=_highlights(where, raw.get("highlight")),
        crop=crop.strip() if crop else None,
        status=status,
        frame=_merge_section(where + ".frame", defaults["frame"], raw.get("frame"), _FRAME_KEYS),
        diff=_merge_section(where + ".diff", defaults["diff"], raw.get("diff"), _DIFF_KEYS),
    )


def _validate_numbers(where: str, frame: dict[str, Any], diff: dict[str, Any]) -> None:
    for key in _FRAME_KEYS:
        if not isinstance(frame.get(key), int) or frame[key] < 0:
            raise _fail(where, f"frame.{key} must be a non-negative integer")
    tol = diff.get("tolerance")
    if not isinstance(tol, int) or not 0 <= tol <= 255:
        raise _fail(where, "diff.tolerance must be an integer 0..255")
    thr = diff.get("threshold")
    if not isinstance(thr, (int, float)) or not 0 <= thr <= 1:
        raise _fail(where, "diff.threshold must be a number 0..1")


def parse_manifest(data: Any, path: Path) -> Manifest:
    if not isinstance(data, dict):
        raise _fail("top level", "must be a mapping")
    _check_keys("top level", data, {"defaults", "global_sources", "entries"})
    raw_defaults = data.get("defaults") or {}
    if not isinstance(raw_defaults, dict):
        raise _fail("defaults", "must be a mapping")
    _check_keys("defaults", raw_defaults, _DEFAULT_KEYS)
    defaults = dict(BUILTIN_DEFAULTS)
    defaults.update({k: v for k, v in raw_defaults.items() if k not in ("frame", "diff")})
    defaults["frame"] = _merge_section("defaults.frame", BUILTIN_DEFAULTS["frame"], raw_defaults.get("frame"), _FRAME_KEYS)
    defaults["diff"] = _merge_section("defaults.diff", BUILTIN_DEFAULTS["diff"], raw_defaults.get("diff"), _DIFF_KEYS)
    preview = _str_list("defaults.preview_platforms", defaults["preview_platforms"])
    raw_entries = data.get("entries") or []
    if not isinstance(raw_entries, list):
        raise _fail("entries", "must be a list")
    entries = [_resolve_entry(i, raw, defaults) for i, raw in enumerate(raw_entries)]
    seen: dict[str, str] = {}
    targets: dict[tuple[str, str], str] = {}
    for entry in entries:
        _validate_numbers(f"entry {entry.id}", entry.frame, entry.diff)
        if entry.id in seen:
            raise _fail(f"entry {entry.id}", "duplicate id")
        seen[entry.id] = entry.id
        target = (entry.doc, entry.ref.casefold())
        if target in targets:
            raise _fail(f"entry {entry.id}", f"doc/ref already used by {targets[target]}")
        targets[target] = entry.id
    return Manifest(
        path=path,
        defaults=defaults,
        global_sources=_str_list("global_sources", data.get("global_sources")),
        preview_platforms=preview,
        entries=entries,
    )


def load_manifest(path: Path) -> Manifest:
    path = Path(path)
    if not path.exists():
        raise UsageError(f"manifest not found: {path}")
    try:
        data = yaml.safe_load(read_text_exact(path))
    except yaml.YAMLError as exc:
        raise UsageError(f"{path}: invalid YAML: {exc}") from exc
    return parse_manifest(data, path)


# Top-level scripts that prepare a run but never touch what is rendered.
NOT_PIPELINE = frozenset({"shoot.py"})


def pipeline_files(pipeline_dir: Path = SCRIPT_DIR) -> dict[str, str]:
    """sha256 of every pipeline file: top-level *.py plus requirements.txt.

    Tests live under tests/ and are not part of the pipeline, nor is
    anything in NOT_PIPELINE.
    """
    pipeline_dir = Path(pipeline_dir)
    files = sorted(f for f in pipeline_dir.glob("*.py") if f.name not in NOT_PIPELINE)
    req = pipeline_dir / "requirements.txt"
    if req.exists():
        files.append(req)
    return {f.name: sha256_file(f) for f in files}


def inputs_hash(entry: Entry, processing: dict[str, Any], pipeline_dir: Path = SCRIPT_DIR) -> str:
    """sha256 over resolved render settings, pipeline files and post-processing.

    `processing` carries the optimizer in use (`oxipng <version>` or `none`)
    and the encoder versions; see postprocess.processing_descriptor().
    """
    settings = entry.settings()
    for key in _NON_RENDER_KEYS:
        settings.pop(key, None)
    payload = {
        "entry": settings,
        "frame": dict(entry.frame),
        "diff": dict(entry.diff),
        "pipeline": pipeline_files(pipeline_dir),
        "processing": processing,
    }
    return sha256_bytes(canonical_json(payload))
