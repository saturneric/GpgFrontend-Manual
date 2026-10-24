from __future__ import annotations

import shutil
import unittest
from pathlib import Path

from helpers import World, short_tempdir, write

import docrefs
from common import PipelineError

TREE = {
    "src/content/docs/one.md": (
        "![A][img-1]\n"
        "![again][img-1]\n"
        "Text ![inline](https://cdn.example.org/i/x.png \"t\") more\n"
        "<img src=\"https://cdn.example.org/i/shared.webp\" alt=\"h\">\n"
        "```md\n![not an image][img-2]\n```\n"
        "`![code span][img-2]`\n"
        "\n"
        "[img-1]:\n"
        "    https://cdn.example.org/i/one.gif\n"
        "[other]: https://example.org/\n"
    ),
    "src/content/docs/sub/two.mdx": (
        "<Tabs>\n  ![][img-1]\n</Tabs>\n![shot][]\n![missing][img-7]\n![empty][img-3]\n"
        "[img-1]: https://cdn.example.org/i/shared.webp\n"
        "[shot]: <https://cdn.example.org/i/shot.WEBP>\n"
        "[img-3]: TODO\n"
    ),
    "src/content/docs/none.md": "No images here. [link][x]\n\n[x]: https://example.org/\n",
}


class ParseTest(unittest.TestCase):
    def test_reference_inline_html_and_code_skipping(self) -> None:
        page = docrefs.scan_text("one.md", TREE["src/content/docs/one.md"])
        kinds = [(r.kind, r.label, r.line) for r in page.refs]
        self.assertEqual(kinds, [("reference", "img-1", 1), ("reference", "img-1", 2),
                                 ("inline", None, 3), ("html", None, 4)])
        self.assertEqual(page.refs[2].url, "https://cdn.example.org/i/x.png")
        self.assertEqual(page.refs[3].url, "https://cdn.example.org/i/shared.webp")

    def test_wrapped_definition(self) -> None:
        page = docrefs.scan_text("one.md", TREE["src/content/docs/one.md"])
        d = page.definition_for("IMG-1")
        self.assertEqual(d.url, "https://cdn.example.org/i/one.gif")
        self.assertEqual((d.line_start, d.line_end), (10, 11))
        self.assertTrue(d.text.startswith("[img-1]:\n    https://"))

    def test_collapsed_angle_and_todo(self) -> None:
        page = docrefs.scan_text("two.mdx", TREE["src/content/docs/sub/two.mdx"])
        self.assertEqual(page.definition_for("shot").url, "https://cdn.example.org/i/shot.WEBP")
        self.assertIsNone(page.definition_for("img-7"))
        self.assertTrue(docrefs.is_missing_url(page.definition_for("img-3").url))


class InventoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = short_tempdir("gfinv")
        self.addCleanup(shutil.rmtree, self.root, True)
        for rel, text in TREE.items():
            write(self.root / rel, text)

    def test_counts_match_fixture(self) -> None:
        pages = docrefs.scan_docs(self.root)
        inv = docrefs.inventory(pages, {("src/content/docs/one.md", "img-1"): "managed-one"})
        by_doc = {p["doc"]: p for p in inv["pages"]}
        one = by_doc["src/content/docs/one.md"]
        # img-1 twice, one inline, one <img>; one definition is used.
        self.assertEqual((one["references"], one["definitions"], one["unique_urls"]), (4, 1, 3))
        self.assertEqual(one["formats_by_reference"], {"gif": 2, "png": 1, "webp": 1})
        two = by_doc["src/content/docs/sub/two.mdx"]
        # img-1, shot, img-7 (no definition), img-3 (TODO): 3 definitions, 2 real URLs.
        self.assertEqual((two["references"], two["definitions"], two["unique_urls"]), (4, 3, 2))
        self.assertEqual(two["formats_by_reference"], {"(none)": 2, "webp": 2})
        total = inv["total"]
        self.assertEqual(total["pages_with_images"], 2)
        self.assertEqual(total["references"], 8)
        self.assertEqual(total["definitions"], 4)
        # shared.webp appears on both pages and is counted once.
        self.assertEqual(total["unique_urls"], 4)
        self.assertEqual(total["formats_by_unique_url"], {"gif": 1, "png": 1, "webp": 2})
        managed = [r for r in inv["refs"] if r["managed_id"]]
        self.assertEqual(len(managed), 2)
        self.assertEqual(len(inv["refs"]), 8)


class RewriteTest(unittest.TestCase):
    def test_only_the_url_token_changes_and_crlf_survives(self) -> None:
        text = "a\r\n![][img-1]\r\n\r\n[img-1]: https://old.example/x.webp \"title\"\r\n[img-2]: https://keep/y\r\n"
        out = docrefs.replace_definition_url(text, "img-1", "https://new.example/z.webp", "https://old.example/x.webp")
        self.assertEqual(out, text.replace("https://old.example/x.webp", "https://new.example/z.webp"))
        self.assertEqual(out.count("\r\n"), text.count("\r\n"))

    def test_wrapped_and_empty_definitions(self) -> None:
        wrapped = "[img-1]:\n  https://old/a.webp\n"
        self.assertEqual(docrefs.replace_definition_url(wrapped, "img-1", "https://n/b.webp", "https://old/a.webp"),
                         "[img-1]:\n  https://n/b.webp\n")
        empty = "[img-1]:\n\nText\n"
        self.assertEqual(docrefs.replace_definition_url(empty, "img-1", "https://n/b.webp", ""),
                         "[img-1]: https://n/b.webp\n\nText\n")

    def test_refuses_duplicates_and_unexpected_url(self) -> None:
        dup = "[img-1]: https://a/1\n[img-1]: https://a/2\n"
        with self.assertRaises(PipelineError):
            docrefs.replace_definition_url(dup, "img-1", "https://n/x", "https://a/1")
        with self.assertRaises(PipelineError):
            docrefs.replace_definition_url("[img-1]: https://a/1\n", "img-1", "https://n/x", "https://a/9")


class CheckRefStatusTest(World):
    def test_unmanaged_orphan_missing_and_manual_only(self) -> None:
        write(self.manual / "src/content/docs/guides/c.md", "![x][img-1]\n![y](https://cdn/z.png)\n")
        rows = self.check_rows()
        self.assertEqual(rows["src/content/docs/guides/c.md#img-1"], ["unmanaged", "missing"])
        self.assertIn("unmanaged", rows["src/content/docs/guides/c.md#None"])
        # manual-shot points at img-9, which b.md does not use.
        self.assertEqual(rows["manual-shot"], ["orphan", "manual-only"])
        self.assertIn("missing", rows["a-main"])  # no lock record yet
        self.assertIn("env-unchecked", rows["a-main"])


if __name__ == "__main__":
    unittest.main()
