"""Environment record hashing, per the C++/Python contract.

env_hash_core is computed by the binary and recomputed here; both must agree.
The final env_hash adds the platform tag and the font file hashes, which only
the Python side knows.
"""

from __future__ import annotations

import math
from typing import Any

from common import PipelineError, canonical_json, sha256_bytes

ENV_SCHEMA = 1

# Recorded but never hashed. The first two also vary between two runs on the
# same machine, so they are dropped from the lock and from repeat comparisons.
RUN_VOLATILE_KEYS = ("display", "profile_path")


def _int(value: Any, where: str) -> int:
    """Pixel, DPR and DPI values are hashed as integers.

    Non-integral floats are rounded half away from zero, which matches
    qRound() on the C++ side for the non-negative values involved.
    """
    if isinstance(value, bool):
        raise PipelineError(f"env record: {where} must be a number")
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(math.floor(value + 0.5)) if value >= 0 else -int(math.floor(-value + 0.5))
    raise PipelineError(f"env record: {where} must be a number, got {value!r}")


def core_subset(env: dict[str, Any]) -> dict[str, Any]:
    try:
        os_info = env["os"]
        screen = env["screen"]
        size = screen["size"]
        return {
            "os": {"product": os_info["product"], "build": os_info["build"]},
            "qt_version": env["qt_version"],
            "platform_name": env["platform_name"],
            "screen": {
                "size": [_int(size[0], "screen.size"), _int(size[1], "screen.size")],
                "dpr": _int(screen["dpr"], "screen.dpr"),
                "logical_dpi": _int(screen["logical_dpi"], "screen.logical_dpi"),
                "physical_dpi": _int(screen["physical_dpi"], "screen.physical_dpi"),
            },
            "style": env["style"],
            "color_scheme": env["color_scheme"],
            "locale": env["locale"],
            "clock": env["clock"],
            "font_requested": list(env["font_requested"]),
            "font_resolved": list(env["font_resolved"]),
            "system_font": env["system_font"],
            "gnupg_version": env["gnupg_version"],
            "gpgme_version": env["gpgme_version"],
            "gpg_clock": env["gpg_clock"],
            "tz_offset_check": _int(env["tz_offset_check"], "tz_offset_check"),
        }
    except (KeyError, IndexError, TypeError) as exc:
        raise PipelineError(f"env record incomplete: {exc!r}") from exc


def canonical_core(env: dict[str, Any]) -> bytes:
    return canonical_json(core_subset(env))


def env_hash_core(env: dict[str, Any]) -> str:
    return sha256_bytes(canonical_core(env))


def font_file_list(env: dict[str, Any]) -> list[str]:
    """Families whose files are hashed: font_resolved order, then system_font."""
    families = list(env.get("font_resolved") or [])
    families.append(env.get("system_font") or "")
    return families


def final_env_hash(core_hash: str, platform: str, font_files: list[dict[str, Any]]) -> str:
    payload = {
        "core": core_hash,
        "platform": platform,
        "font_files": [{"family": f["family"], "sha256": f.get("sha256")} for f in font_files],
    }
    return sha256_bytes(canonical_json(payload))


def _windows_build(env: dict[str, Any]) -> int:
    digits = "".join(ch if ch.isdigit() else " " for ch in str(env.get("os", {}).get("build", "")))
    numbers = [int(part) for part in digits.split()]
    return max(numbers) if numbers else 0


def platform_tag(env: dict[str, Any], under_xvfb: bool) -> str:
    """windows11, linux-xvfb, or a descriptive non-reference tag."""
    name = str(env.get("platform_name", ""))
    if name == "windows":
        product = str(env.get("os", {}).get("product", ""))
        if "Windows 11" in product or _windows_build(env) >= 22000:
            return "windows11"
        return "windows-other"
    if name == "xcb":
        return "linux-xvfb" if under_xvfb else "linux-xcb"
    return f"other-{name or 'unknown'}"


def strip_volatile(env: dict[str, Any]) -> dict[str, Any]:
    """The env as stored in the committed lock: no temp paths or display ids."""
    return {k: v for k, v in env.items() if k not in RUN_VOLATILE_KEYS}
