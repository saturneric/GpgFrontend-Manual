from __future__ import annotations

import copy
import json
import os
import unittest
from pathlib import Path

import helpers  # noqa: F401  (sets sys.path)

import envhash

# The fixture is owned by the C++ side; its own test checks the same values.
GPGFRONTEND = Path(os.environ.get("GF_SHOTS_GPGFRONTEND",
                                  str(helpers.PIPELINE_DIR.parents[2] / "GpgFrontend")))
CROSS_CHECK_FIXTURE = GPGFRONTEND / "resource" / "screenshot" / "env-hash-fixture.json"


def sample_env() -> dict:
    return {
        "schema": 1,
        "os": {"product": "Windows 11 Pro", "kernel": "10.0.26100", "build": "26100"},
        "qt_version": "6.8.2", "platform_name": "windows",
        "screen": {"name": "DISPLAY1", "size": [2560, 1600], "geometry": [0, 0, 2560, 1600],
                   "dpr": 2, "logical_dpi": 96, "physical_dpi": 96.4},
        "style": "windows11", "color_scheme": "light", "color_scheme_method": "hint",
        "locale": "en_US", "clock": "2026-01-15T10:00:00Z",
        "font_requested": ["Noto Sans", "思源黑体"], "font_resolved": ["Noto Sans", "思源黑体"],
        "system_font": "Segoe UI", "gnupg_version": "2.4.7", "gpgme_version": "1.24.2",
        "gpg_clock": {"gpg_conf": "applied", "agent_conf": "applied"},
        "ui_clock_probe": "ok", "gpg_clock_probe": "ok", "tz_offset_check": 0,
        "build_commit": "abc", "display": ":99", "profile_path": "/tmp/x/.tmp-1", "gate_failures": [],
    }


FONTS = [{"family": "Noto Sans", "sha256": "aa"}, {"family": "思源黑体", "sha256": "bb"},
         {"family": "Segoe UI", "sha256": "cc"}]


def final(env: dict, fonts: list = FONTS, platform: str = "windows11") -> str:
    return envhash.final_env_hash(envhash.env_hash_core(env), platform, fonts)


class CrossCheckTest(unittest.TestCase):
    def test_cpp_fixture_reproduces_byte_for_byte(self) -> None:
        if not CROSS_CHECK_FIXTURE.exists():
            self.skipTest(f"C++ fixture not found at {CROSS_CHECK_FIXTURE} (set GF_SHOTS_GPGFRONTEND)")
        fixture = json.loads(CROSS_CHECK_FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(envhash.canonical_core(fixture["env"]).decode("utf-8"), fixture["canonical"])
        self.assertEqual(envhash.env_hash_core(fixture["env"]), fixture["env_hash_core"])
        self.assertEqual(envhash.platform_tag(fixture["env"], under_xvfb=False), "windows11")

    def test_canonical_form_is_compact_sorted_utf8(self) -> None:
        text = envhash.canonical_core(sample_env()).decode("utf-8")
        self.assertTrue(text.startswith('{"clock":"2026-01-15T10:00:00Z","color_scheme":"light"'))
        self.assertIn('"思源黑体"', text)  # ensure_ascii=False
        self.assertIn('"physical_dpi":96,', text)  # DPI hashed as an integer
        self.assertNotIn(" ", text.replace("Noto Sans", "").replace("Segoe UI", "").replace("Windows 11 Pro", ""))


class HashSensitivityTest(unittest.TestCase):
    def test_key_order_and_volatile_fields_do_not_matter(self) -> None:
        base = final(sample_env())
        reordered = dict(reversed(list(sample_env().items())))
        self.assertEqual(final(reordered), base)
        env = sample_env()
        env.update(display=":42", profile_path="/tmp/other/.tmp-2", build_commit="zzz",
                   color_scheme_method="palette")
        env["screen"]["name"] = "OTHER"
        env["screen"]["geometry"] = [100, 50, 2560, 1600]
        env["os"]["kernel"] = "6.1"
        self.assertEqual(final(env), base)

    def test_render_relevant_changes_do(self) -> None:
        base = final(sample_env())
        for key, value in (("color_scheme", "dark"), ("locale", "zh_CN"), ("clock", "2026-02-01T10:00:00Z")):
            env = sample_env()
            env[key] = value
            self.assertNotEqual(final(env), base, key)
        env = sample_env()
        env["font_requested"] = ["Noto Sans"]
        self.assertNotEqual(final(env), base)
        fonts = copy.deepcopy(FONTS)
        fonts[1]["sha256"] = "changed"
        self.assertNotEqual(final(sample_env(), fonts), base)
        self.assertNotEqual(final(sample_env(), platform="linux-xvfb"), base)

    def test_platform_tags(self) -> None:
        env = sample_env()
        self.assertEqual(envhash.platform_tag(env, False), "windows11")
        env["os"] = {"product": "Windows 10", "build": "19045"}
        self.assertEqual(envhash.platform_tag(env, False), "windows-other")
        env["platform_name"] = "xcb"
        self.assertEqual(envhash.platform_tag(env, True), "linux-xvfb")
        self.assertEqual(envhash.platform_tag(env, False), "linux-xcb")

    def test_lock_env_drops_run_volatile_fields(self) -> None:
        stripped = envhash.strip_volatile(sample_env())
        self.assertNotIn("profile_path", stripped)
        self.assertNotIn("display", stripped)
        self.assertIn("build_commit", stripped)


if __name__ == "__main__":
    unittest.main()
