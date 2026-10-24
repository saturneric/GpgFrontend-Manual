"""A stand-in for the GpgFrontend screenshot-mode binary, following the contract.

Behaviour is driven by the JSON file named in $FAKEGF_CONFIG:
  platform_name, product, build   env record values ("windows" by default)
  exit             {scenario-or-"env": code} forced exit codes
  variant          int; shifts every pixel's red channel (a changed render)
  tweak_pixels     int; recolours this many pixels by a small amount
  nondeterministic bool; every run differs
  write_appdata    path; a file is created there (footprint test)
  write_appdata_render_only  bool; only renders write it, probes do not
  missing          list of widget names reported as missing
  gate_failures    list; written into the env record with exit 6
  log              path; one line per invocation is appended
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PIL import Image, ImageDraw  # noqa: E402

import envhash  # noqa: E402

SCENARIOS = {
    "main-window": ("1100x680", "window"),
    "key-generate-dialog": ("auto", "dialog"),
    "text-decrypt-verify-result": ("1100x680", "window"),
    "main-window-menu-popup": ("1100x680", "composite"),
    "demo": ("320x200", "window"),
}


def config() -> dict:
    path = os.environ.get("FAKEGF_CONFIG")
    if path and Path(path).exists():
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return {}


def env_record(args: argparse.Namespace, cfg: dict) -> dict:
    fonts = [f for f in args.font_family.split(",") if f]
    record = {
        "schema": 1,
        "os": {"product": cfg.get("product", "Windows 11 Pro"), "kernel": "10.0.26100",
               "build": cfg.get("build", "26100")},
        "qt_version": "6.8.2",
        "platform_name": cfg.get("platform_name", "windows"),
        "screen": {"name": "FAKE-1", "size": [2560, 1600], "geometry": [0, 0, 2560, 1600],
                   "dpr": 2, "logical_dpi": 96, "physical_dpi": 96},
        "style": "windows11",
        "color_scheme": args.theme,
        "locale": args.locale,
        "clock": args.clock,
        "font_requested": fonts,
        "font_resolved": fonts,
        "system_font": "Segoe UI",
        "gnupg_version": "2.4.7",
        "gpgme_version": "1.24.2",
        "gpg_clock": {"gpg_conf": "applied", "agent_conf": "applied"},
        "ui_clock_probe": "ok",
        "gpg_clock_probe": "ok",
        "tz_offset_check": 0,
        "build_commit": "fake",
        "display": os.environ.get("DISPLAY", ""),
        "profile_path": os.path.join(os.environ.get("TMPDIR", "/tmp"), f".tmp-{random.getrandbits(64):016x}"),
        "gate_failures": list(cfg.get("gate_failures", [])),
        "color_scheme_method": "hint",
    }
    record["env_hash_core"] = envhash.env_hash_core(record)
    return record


def render(args: argparse.Namespace, cfg: dict, out: Path) -> dict:
    size = args.size or "120x90"  # the natural size of an "auto" scenario
    w, h = (int(v) * 2 for v in size.split("x"))
    base = (240, 240, 240) if args.theme == "light" else (32, 32, 36)
    red = (base[0] + int(cfg.get("variant", 0))) % 256
    if cfg.get("nondeterministic"):
        red = random.randrange(256)
    img = Image.new("RGBA", (w, h), (red, base[1], base[2], 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle((4, 4, w // 3, h // 3), fill=(30, 120, 220, 255))
    for i in range(int(cfg.get("tweak_pixels", 0))):
        x, y = w // 4 + i % (w // 2), h // 2 + i // (w // 2)
        r, g, b, a = img.getpixel((x, y))
        img.putpixel((x, y), (min(255, r + 30), g, b, a))
    img.save(out, format="PNG")
    mode = SCENARIOS.get(args.screenshot, ("", "window"))[1]
    widgets = {
        "InfoBoardWidget": {"rect": [10, h // 2, w - 20, h // 2 - 10], "clipped": False},
        "importKeyMenu": {"rect": [w // 2, 10, w // 4, 20], "clipped": False},
        "nameEdit": {"rect": [10, 10, w // 3, 20], "clipped": False},
    }
    missing = list(cfg.get("missing", []))
    for name in missing:
        widgets.pop(name, None)
    return {"schema": 1, "scenario": args.screenshot, "capture_mode": mode, "dpr": 2,
            "image_size": [w, h], "origin": [0, 0], "layers": [{"name": "window", "rect": [0, 0, w, h]}],
            "widgets": widgets, "missing": missing, "error": None}


def main() -> int:
    cfg = config()
    if cfg.get("log"):
        with open(cfg["log"], "a", encoding="utf-8") as handle:
            handle.write(" ".join(sys.argv[1:]) + "\n")
    if "--screenshot-list" in sys.argv:
        for name, (size, mode) in SCENARIOS.items():
            print(f"{name}\t{size}\t{mode}")
        return 0
    p = argparse.ArgumentParser()
    p.add_argument("--temp-profile", action="store_true")
    p.add_argument("--screenshot")
    p.add_argument("--screenshot-env", action="store_true")
    for opt in ("locale", "theme", "size", "font-family", "clock", "demo-gnupghome", "fixtures", "out", "timeout"):
        p.add_argument(f"--{opt}")
    args = p.parse_args()
    if not args.temp_profile:
        return 2
    if cfg.get("write_appdata") and not (cfg.get("write_appdata_render_only") and args.screenshot_env):
        Path(cfg["write_appdata"]).mkdir(parents=True, exist_ok=True)
        (Path(cfg["write_appdata"]) / "leak.txt").write_text("x", encoding="utf-8")
    out = Path(args.out)
    record = env_record(args, cfg)
    key = "env" if args.screenshot_env else args.screenshot
    forced = cfg.get("exit", {}).get(key)
    if record["gate_failures"]:
        forced = 6
    if args.screenshot_env:
        if forced:
            record["error"] = {"code": forced, "reason": "forced", "detail": "fake"}
        out.write_text(json.dumps(record), encoding="utf-8")
        return forced or 0
    if forced:
        partial = {"schema": 1, "scenario": args.screenshot, "env": record,
                   "error": {"code": forced, "reason": "forced-failure", "detail": "fake"}}
        out.with_suffix(".json").write_text(json.dumps(partial), encoding="utf-8")
        return forced
    geometry = render(args, cfg, out)
    geometry["env"] = record
    out.with_suffix(".json").write_text(json.dumps(geometry), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
