"""Compares a new post-processed PNG with the local baseline.

The baseline `.screenshots-cache/baseline/<id>.png` only counts when its
pixels hash equals the lock's `pixels_sha256`. It is never fetched from the CDN.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from PIL import Image, ImageChops

from postprocess import pixels_sha256

NEW = "new"
REPLACE = "replace"
UNCHANGED = "unchanged"
BASELINE_UNAVAILABLE = "baseline-unavailable"


@dataclass
class DiffResult:
    result: str
    changed_ratio: Optional[float] = None
    detail: str = ""


def baseline_path(cache: Path, entry_id: str) -> Path:
    return Path(cache) / "baseline" / f"{entry_id}.png"


def baseline_valid(cache: Path, entry_id: str, lock_record: Optional[dict[str, Any]]) -> bool:
    if not lock_record:
        return False
    path = baseline_path(cache, entry_id)
    if not path.is_file():
        return False
    try:
        with Image.open(path) as img:
            return pixels_sha256(img) == lock_record.get("pixels_sha256")
    except OSError:
        return False


def changed_ratio(new: Image.Image, old: Image.Image, tolerance: int) -> float:
    """Share of pixels whose largest per-channel delta exceeds `tolerance`."""
    delta = ImageChops.difference(new.convert("RGBA"), old.convert("RGBA"))
    bands = delta.split()
    worst = bands[0]
    for band in bands[1:]:
        worst = ImageChops.lighter(worst, band)
    changed = worst.point(lambda v: 255 if v > tolerance else 0).histogram()[255]
    return changed / float(new.size[0] * new.size[1])


def compare(new_png: Path, cache: Path, entry_id: str, lock_record: Optional[dict[str, Any]],
            settings: dict[str, Any]) -> DiffResult:
    if not lock_record:
        return DiffResult(NEW, detail="no lock record")
    if not baseline_valid(cache, entry_id, lock_record):
        path = baseline_path(cache, entry_id)
        why = "baseline missing" if not path.exists() else "baseline pixels_sha256 differs from the lock"
        return DiffResult(BASELINE_UNAVAILABLE, detail=why)
    with Image.open(new_png) as new, Image.open(baseline_path(cache, entry_id)) as old:
        if new.size != old.size:
            return DiffResult(REPLACE, 1.0, f"size {old.size} -> {new.size}")
        ratio = changed_ratio(new, old, int(settings["tolerance"]))
    if ratio > float(settings["threshold"]):
        return DiffResult(REPLACE, ratio, f"{ratio:.6f} of pixels changed")
    return DiffResult(UNCHANGED, ratio, f"{ratio:.6f} of pixels changed")
