"""Finds the font file a family name resolves to, and hashes it.

Windows: the HKLM and HKCU `...\\Windows NT\\CurrentVersion\\Fonts` registry
keys. Linux and others: `fc-match`.

Limit: Qt does not expose which file it used for each glyph, so glyph-level
fallback outside the listed families cannot be observed here.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional

from common import sha256_file

FontResolver = Callable[[str], Optional[Path]]

_REG_SUFFIX_RE = re.compile(r"\s*\((TrueType|OpenType|All res)\)\s*$", re.IGNORECASE)
_STYLE_WORDS = {
    "regular", "book", "normal", "roman", "medium", "bold", "italic", "oblique",
    "light", "thin", "black", "heavy", "semibold", "extrabold", "extralight",
    "demibold", "ultralight", "condensed", "semicondensed",
}
_FONTS_KEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"


def _fc_escape(family: str) -> str:
    return re.sub(r"([\\\-:,])", r"\\\1", family)


def resolve_fc_match(family: str) -> Optional[Path]:
    exe = shutil.which("fc-match")
    if not exe or not family:
        return None
    try:
        out = subprocess.run(
            [exe, "-f", "%{file}", _fc_escape(family)],
            capture_output=True, timeout=30, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    path = out.stdout.decode("utf-8", "replace").strip()
    return Path(path) if path and Path(path).is_file() else None


def _registry_fonts() -> list[tuple[str, str]]:
    import winreg  # type: ignore[import-not-found]

    found: list[tuple[str, str]] = []
    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            key = winreg.OpenKey(hive, _FONTS_KEY)
        except OSError:
            continue
        with key:
            index = 0
            while True:
                try:
                    name, data, _ = winreg.EnumValue(key, index)
                except OSError:
                    break
                index += 1
                if isinstance(data, str):
                    found.append((name, data))
    return found


def match_registry(family: str, values: list[tuple[str, str]]) -> Optional[str]:
    """Picks the registry file for `family`: the regular face if listed,
    else the first style face in name order. Pure, so it is testable."""
    wanted = family.casefold()
    exact: list[tuple[str, str]] = []
    styled: list[tuple[str, str]] = []
    for name, data in values:
        for face in _REG_SUFFIX_RE.sub("", name).split(" & "):
            face_cf = face.strip().casefold()
            if face_cf in (wanted, wanted + " regular"):
                exact.append((face_cf, data))
            elif face_cf.startswith(wanted + " "):
                rest = face_cf[len(wanted) + 1:].split()
                if rest and all(word in _STYLE_WORDS for word in rest):
                    styled.append((face_cf, data))
    for group in (exact, styled):
        if group:
            return sorted(group)[0][1]
    return None


def resolve_windows(family: str) -> Optional[Path]:
    data = match_registry(family, _registry_fonts())
    if not data:
        return None
    path = Path(data)
    if not path.is_absolute():
        path = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / data
    return path if path.is_file() else None


def resolve_font_file(family: str) -> Optional[Path]:
    if sys.platform == "win32":
        return resolve_windows(family)
    return resolve_fc_match(family)


def font_files(families: list[str], resolver: FontResolver = resolve_font_file,
               cache: Optional[dict[str, dict]] = None) -> list[dict]:
    """[{family, file, sha256}] in the given order; sha256 is None when the
    family resolves to no file."""
    out = []
    for family in families:
        if cache is not None and family in cache:
            out.append(dict(cache[family]))
            continue
        path = resolver(family) if family else None
        record = {
            "family": family,
            "file": path.name if path else None,
            "sha256": sha256_file(path) if path else None,
        }
        if cache is not None:
            cache[family] = record
        out.append(dict(record))
    return out
