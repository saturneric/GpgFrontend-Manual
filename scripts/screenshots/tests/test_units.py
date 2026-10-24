"""Post-processing, manifest, render runner, upload parsing and font lookup."""

from __future__ import annotations

import shutil
import unittest
from pathlib import Path

from PIL import Image

from helpers import MANIFEST, World, short_tempdir, write

import fonts
import postprocess
import upload
from common import UsageError
from manifest import Highlight, load_manifest, parse_manifest
from render import RenderConfig, Renderer, check_geometry


def geometry(w: int, h: int, **extra) -> dict:
    g = {"schema": 1, "capture_mode": "window", "dpr": 2, "image_size": [w, h], "origin": [0, 0],
         "layers": [], "widgets": {"box": {"rect": [20, 20, 60, 30], "clipped": False}}, "missing": ["gone"],
         "error": None}
    g.update(extra)
    return g


class PostprocessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = short_tempdir("gfpp")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.raw = self.tmp / "raw.png"
        Image.new("RGBA", (200, 120), (240, 240, 240, 255)).save(self.raw)
        manifest = parse_manifest(__import__("yaml").safe_load(MANIFEST), Path("m.yaml"))
        self.entry = manifest.by_id()["a-main"]

    def entry_with(self, *highlights: Highlight):
        from dataclasses import replace
        return replace(self.entry, highlight=tuple(highlights))

    def test_frame_size_shadow_and_corners(self) -> None:
        out = postprocess.process(self.raw, geometry(200, 120), self.entry_with(), self.tmp, "a")
        pad = self.entry.frame["padding"] * 2
        with Image.open(out.png) as img:
            self.assertEqual(img.size, (200 + 2 * pad, 120 + 2 * pad))
            self.assertEqual(img.getpixel((0, 0))[3], 0)  # transparent padding
            self.assertEqual(img.getpixel((pad, pad))[3] < 255, True)  # rounded corner
            self.assertEqual(img.getpixel((pad + 100, pad + 60)), (240, 240, 240, 255))
            below = img.getpixel((pad + 100, pad + 120 + 4))
            self.assertGreater(below[3], 0)  # shadow under the content

    def test_highlights_box_and_arrow_draw(self) -> None:
        plain = postprocess.process(self.raw, geometry(200, 120), self.entry_with(), self.tmp, "p")
        boxed = postprocess.process(self.raw, geometry(200, 120), self.entry_with(Highlight("box")), self.tmp, "b")
        arrow = postprocess.process(self.raw, geometry(200, 120), self.entry_with(Highlight("box", "arrow")),
                                    self.tmp, "r")
        self.assertEqual(len({plain.pixels_sha256, boxed.pixels_sha256, arrow.pixels_sha256}), 3)

    def test_unknown_or_missing_highlight_fails(self) -> None:
        for name, reason in (("gone", "highlight-missing"), ("nowhere", "highlight-unknown")):
            with self.assertRaises(postprocess.PostprocessError) as ctx:
                postprocess.process(self.raw, geometry(200, 120), self.entry_with(Highlight(name)), self.tmp, "x")
            self.assertEqual(ctx.exception.reason, reason)

    def test_deterministic_and_webp_lossless(self) -> None:
        a = postprocess.process(self.raw, geometry(200, 120), self.entry_with(Highlight("box")), self.tmp / "1", "a")
        b = postprocess.process(self.raw, geometry(200, 120), self.entry_with(Highlight("box")), self.tmp / "2", "a")
        self.assertEqual((a.png_sha256, a.webp_sha256, a.pixels_sha256), (b.png_sha256, b.webp_sha256, b.pixels_sha256))
        with Image.open(a.webp) as webp:
            self.assertEqual(postprocess.pixels_sha256(webp), a.pixels_sha256)

    def test_dpr_and_size_mismatch(self) -> None:
        with self.assertRaises(postprocess.PostprocessError):
            postprocess.process(self.raw, geometry(200, 120, dpr=1), self.entry, self.tmp, "x")
        with self.assertRaises(postprocess.PostprocessError):
            postprocess.process(self.raw, geometry(201, 120), self.entry, self.tmp, "x")

    def test_optimizer_descriptor(self) -> None:
        desc = postprocess.processing_descriptor()
        self.assertIn(desc["optimizer"], ("none",) if not shutil.which("oxipng") else (desc["optimizer"],))
        self.assertTrue(desc["pillow"])


class ManifestTest(unittest.TestCase):
    def load(self, text: str):
        return parse_manifest(__import__("yaml").safe_load(text), Path("m.yaml"))

    def test_defaults_resolution_and_auto_size(self) -> None:
        m = self.load("entries:\n  - {id: x, doc: d.md, ref: img-1, scenario: s, size: auto}\n"
                      "  - {id: y, doc: d.md, ref: img-2, scenario: s, highlight: [a, {name: b, style: arrow}]}\n")
        x, y = m.entries
        self.assertIsNone(x.size)
        self.assertEqual(x.size_str, "auto")
        self.assertEqual(y.size, (1280, 960))
        self.assertEqual(y.fonts, ("Noto Sans", "Noto Sans CJK SC"))
        self.assertEqual(y.highlight, (Highlight("a"), Highlight("b", "arrow")))
        self.assertEqual(y.diff, {"tolerance": 16, "threshold": 0.001})

    def test_rejects_bad_input(self) -> None:
        bad = [
            "entries:\n  - {id: x, doc: d.md, ref: r, scenario: s, clock: '2026-01-15 10:00'}\n",
            "entries:\n  - {id: x, doc: d.md, ref: r, scenario: s, size: big}\n",
            "entries:\n  - {id: x, doc: d.md, ref: r, scenario: s, typo: 1}\n",
            "entries:\n  - {id: x, doc: d.md, ref: r}\n",
            "entries:\n  - {id: x, doc: d.md, ref: r, scenario: s}\n  - {id: x, doc: e.md, ref: r, scenario: s}\n",
            "entries:\n  - {id: x, doc: d.md, ref: r, scenario: s, platform: macos}\n",
            "entries:\n  - {id: x, doc: d.md, ref: r, scenario: s, highlight: {name: a, style: circle}}\n",
        ]
        for text in bad:
            with self.assertRaises(UsageError, msg=text):
                self.load(text)

    def test_real_manifest_loads(self) -> None:
        m = load_manifest(Path(__file__).resolve().parents[1] / "screenshots.yaml")
        self.assertEqual([e.id for e in m.entries], ["main-window", "key-generate-dialog",
                                                      "text-decrypt-verify-result", "main-window-menu-popup"])


class RendererTest(World):
    def renderer(self, **kw) -> Renderer:
        return Renderer(RenderConfig(self.binary, self.gf, self.work_root, **kw))

    def entry(self, entry_id: str = "a-main"):
        return load_manifest(self.manifest).by_id()[entry_id]

    def test_exit_codes_map_to_reasons_with_partial_record(self) -> None:
        for code, reason in ((3, "timeout"), (5, "unexpected-modal"), (4, "output-unwritable")):
            self.set_fake({"exit": {"main-window": code}})
            outcome = self.renderer().render(self.entry(), self.tmp / "out")
            self.assertFalse(outcome.ok)
            self.assertEqual((outcome.exit_code, outcome.reason), (code, reason))
            self.assertIn("forced-failure", outcome.detail)

    def test_auto_size_omits_size_flag(self) -> None:
        from dataclasses import replace
        r = self.renderer()
        cmd = r.command(replace(self.entry(), size=None), self.tmp / "x.png", probe=False)
        self.assertNotIn("--size", cmd)
        self.assertIn("--size", r.command(self.entry(), self.tmp / "x.png", probe=True))

    def test_isolated_environment(self) -> None:
        import os
        os.environ["GNUPGHOME"] = "/real/gnupg"
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        r = self.renderer()
        work = r._new_workdir()
        env = r.subprocess_env(work)
        self.assertNotIn("GNUPGHOME", env)
        self.assertNotIn("QT_QPA_PLATFORM", env)
        if os.name != "nt":
            for var in ("HOME", "XDG_DATA_HOME", "XDG_CONFIG_HOME", "TMPDIR"):
                self.assertTrue(env[var].startswith(str(work)), var)

    def test_long_work_root_is_rejected(self) -> None:
        import os
        if os.name == "nt":
            self.skipTest("Unix socket budget only")
        r = Renderer(RenderConfig(self.binary, self.gf, self.tmp / ("x" * 60)))
        with self.assertRaises(UsageError):
            r._new_workdir()

    def test_env_hash_crosscheck_failure_is_reported(self) -> None:
        import envhash
        real = envhash.env_hash_core
        envhash.env_hash_core = lambda env: "0" * 64
        try:
            outcome = self.renderer().probe(self.entry())
        finally:
            envhash.env_hash_core = real
        self.assertEqual(outcome.reason, "env-invalid")

    def test_screenshot_list(self) -> None:
        listed = self.renderer().list_scenarios()
        self.assertEqual(listed["key-generate-dialog"], {"size": "auto", "capture_mode": "dialog"})


class CheckGeometryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = short_tempdir("gfgeo")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def record(self, image: tuple[int, int], window: list[int]) -> tuple[dict, Path]:
        png = self.tmp / "r.png"
        Image.new("RGBA", image, (240, 240, 240, 255)).save(png)
        return geometry(*image, layers=[{"name": "window", "rect": window}]), png

    def test_window_at_the_requested_size_passes(self) -> None:
        g, png = self.record((2200, 1360), [0, 0, 2200, 1360])
        self.assertEqual(check_geometry(g, png, (1100, 680)), "")

    def test_window_resized_late_is_caught(self) -> None:
        g, png = self.record((2482, 1712), [0, 0, 2482, 1712])
        self.assertIn("size-mismatch", check_geometry(g, png, (1100, 680)))

    def test_composite_checks_the_window_layer_not_the_canvas(self) -> None:
        g, png = self.record((2400, 1360), [0, 0, 2200, 1360])
        g["capture_mode"] = "composite"
        self.assertEqual(check_geometry(g, png, (1100, 680)), "")

    def test_auto_size_skips_the_check(self) -> None:
        g, png = self.record((300, 200), [0, 0, 300, 200])
        self.assertEqual(check_geometry(g, png, None), "")


class UploadParseTest(unittest.TestCase):
    def test_response_validation(self) -> None:
        ok = upload.parse_response('{"result":"success","code":200,"url":"https://i.example/x.webp","del":"https://i/d"}')
        self.assertEqual((ok.url, ok.del_url), ("https://i.example/x.webp", "https://i/d"))
        for raw in ('{"result":"success","url":"http://i.example/x.webp"}', '{"result":"failed"}', "<html>"):
            with self.assertRaises(upload.UploadFailed):
                upload.parse_response(raw)

    def test_credentials_require_https_except_loopback(self) -> None:
        import os
        from unittest import mock
        with mock.patch.dict(os.environ, {"GF_MANUAL_CDN_API": "http://cdn.example.org/api", "GF_MANUAL_CDN_TOKEN": "t"}):
            with self.assertRaises(UsageError):
                upload.credentials_from_env()
        with mock.patch.dict(os.environ, {"GF_MANUAL_CDN_API": "http://127.0.0.1:9/api", "GF_MANUAL_CDN_TOKEN": "t"}):
            self.assertEqual(upload.credentials_from_env().host, "127.0.0.1")


class FontLookupTest(unittest.TestCase):
    def test_registry_matching_prefers_regular(self) -> None:
        values = [
            ("Noto Sans Bold (TrueType)", "NotoSans-Bold.ttf"),
            ("Noto Sans Regular (TrueType)", "NotoSans-Regular.ttf"),
            ("Noto Sans CJK JP Regular & Noto Sans CJK SC Regular (OpenType)", "NotoSansCJK-Regular.ttc"),
            ("Noto Sans CJK SC Bold (OpenType)", "NotoSansCJK-Bold.ttc"),
        ]
        self.assertEqual(fonts.match_registry("Noto Sans", values), "NotoSans-Regular.ttf")
        self.assertEqual(fonts.match_registry("Noto Sans CJK SC", values), "NotoSansCJK-Regular.ttc")
        self.assertIsNone(fonts.match_registry("Noto Serif", values))

    def test_font_files_hash_and_cache(self) -> None:
        tmp = short_tempdir("gffont")
        self.addCleanup(shutil.rmtree, tmp, True)
        f = write(tmp / "A.ttf", "font-bytes")
        calls = []

        def resolver(family):
            calls.append(family)
            return f if family == "A" else None

        cache: dict = {}
        out = fonts.font_files(["A", "B", "A"], resolver, cache)
        self.assertEqual(out[0]["file"], "A.ttf")
        self.assertIsNotNone(out[0]["sha256"])
        self.assertIsNone(out[1]["sha256"])
        self.assertEqual(calls, ["A", "B"])


if __name__ == "__main__":
    unittest.main()
