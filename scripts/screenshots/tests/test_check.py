from __future__ import annotations

import contextlib
import io
import json
import shutil

from helpers import PIPELINE_DIR, World, commit_change, git, write

import check
from manifest import load_manifest, inputs_hash
from postprocess import processing_descriptor
from render import RenderConfig, Renderer


class CheckBaseline(World):
    def write_record(self, entry_id: str, commit: str, env_hash: str = "x", inputs: str | None = None,
                     pipeline_dir=PIPELINE_DIR) -> None:
        entry = load_manifest(self.manifest).by_id()[entry_id]
        lock = self.read_lock()
        lock[entry_id] = {
            "url": "https://cdn.example.org/i/a1.webp", "webp_sha256": "w", "pixels_sha256": "p",
            "gpgfrontend_commit": commit,
            "inputs_hash": inputs or inputs_hash(entry, processing_descriptor(), pipeline_dir),
            "env_hash": env_hash, "env": {}, "generated_at": "2026-01-01T00:00:00Z",
        }
        self.lock.write_text(json.dumps(lock), encoding="utf-8")

    def head(self) -> str:
        return git(self.gf, "rev-parse", "HEAD")


class BaselineStatusTest(CheckBaseline):
    def test_missing_commit_is_unknown_baseline(self) -> None:
        self.write_record("a-main", "0" * 40)
        self.assertIn("unknown-baseline", self.check_rows()["a-main"])

    def test_non_ancestor_commit_is_unknown_baseline(self) -> None:
        git(self.gf, "checkout", "-q", "-b", "side")
        side = commit_change(self.gf, "src/ui/main/MainWindow.cpp", "side\n")
        git(self.gf, "checkout", "-q", "main")
        self.write_record("a-main", side)
        self.assertIn("unknown-baseline", self.check_rows()["a-main"])

    def test_outdated_from_entry_sources(self) -> None:
        self.write_record("a-main", self.head())
        commit_change(self.gf, "src/ui/main/MainWindow.cpp")
        rows = self.check_rows()
        self.assertIn("outdated", rows["a-main"])
        self.assertNotIn("unknown-baseline", rows["a-main"])

    def test_outdated_from_global_sources(self) -> None:
        self.write_record("b-main", self.head())
        commit_change(self.gf, "resource/screenshot/fixtures/decrypt-verify.asc")
        self.assertIn("outdated", self.check_rows()["b-main"])

    def test_unrelated_change_is_not_outdated(self) -> None:
        self.write_record("b-main", self.head())
        commit_change(self.gf, "src/ui/main/MainWindow.cpp")
        self.assertNotIn("outdated", self.check_rows()["b-main"])

    def test_inputs_changed_from_manifest_edit(self) -> None:
        self.write_record("a-main", self.head())
        self.assertNotIn("inputs-changed", self.check_rows()["a-main"])
        text = self.manifest.read_text(encoding="utf-8").replace(
            "    scenario: main-window\n    sources: [src/ui/main/]",
            "    scenario: main-window\n    theme: dark\n    sources: [src/ui/main/]")
        self.manifest.write_text(text, encoding="utf-8")
        self.assertIn("inputs-changed", self.check_rows()["a-main"])

    def test_inputs_changed_from_script_edit(self) -> None:
        pipe = self.tmp / "pipeline"
        pipe.mkdir()
        for f in list(PIPELINE_DIR.glob("*.py")) + [PIPELINE_DIR / "requirements.txt"]:
            shutil.copy(f, pipe / f.name)
        self.write_record("a-main", self.head(), pipeline_dir=pipe)
        self.assertNotIn("inputs-changed", self.check_rows(pipeline_dir=pipe)["a-main"])
        with (pipe / "postprocess.py").open("a", encoding="utf-8") as handle:
            handle.write("\n# tweak\n")
        self.assertIn("inputs-changed", self.check_rows(pipeline_dir=pipe)["a-main"])

    def test_dirty_sources(self) -> None:
        self.write_record("a-main", self.head())
        write(self.gf / "src/ui/main/MainWindow.cpp", "uncommitted\n")
        rows = self.check_rows()
        self.assertIn("dirty-sources", rows["a-main"])
        self.assertNotIn("dirty-sources", rows["b-main"])
        write(self.gf / "src/screenshot/New.cpp", "untracked global source\n")
        self.assertIn("dirty-sources", self.check_rows()["b-main"])


class EnvStatusTest(CheckBaseline):
    def probe_hash(self, entry_id: str) -> str:
        entry = load_manifest(self.manifest).by_id()[entry_id]
        outcome = Renderer(RenderConfig(self.binary, self.gf, self.work_root)).probe(entry)
        self.assertTrue(outcome.ok, outcome.failure)
        return outcome.env.env_hash

    def test_env_unchecked_without_binary(self) -> None:
        self.write_record("a-main", self.head())
        rows = self.check_rows(binary=False)
        self.assertIn("env-unchecked", rows["a-main"])
        self.assertNotIn("ok", rows["a-main"])

    def test_ok_then_env_changed(self) -> None:
        self.write_record("a-main", self.head(), env_hash=self.probe_hash("a-main"))
        self.assertEqual(self.check_rows(binary=True)["a-main"], ["ok"])
        self.set_fake({"build": "26200", "product": "Windows 11 Pro 25H2"})
        self.assertEqual(self.check_rows(binary=True)["a-main"], ["env-changed"])

    def test_platform_mismatch(self) -> None:
        self.set_fake({"platform_name": "xcb", "product": "Debian GNU/Linux 13"})
        rows = self.check_rows(binary=True)
        self.assertIn("platform-mismatch", rows["a-main"])

    def test_probe_runs_once_per_tuple(self) -> None:
        log = self.tmp / "calls.log"
        self.set_fake({"log": str(log)})
        self.check_rows(binary=True)
        probes = [line for line in log.read_text().splitlines() if "--screenshot-env" in line]
        # a-main and b-main share the default tuple; a-dialog has the same tuple too.
        self.assertEqual(len(probes), 1)

    def test_cli_json_and_inventory(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = check.main(["--gpgfrontend", str(self.gf), "--manifest", str(self.manifest), "--lock",
                               str(self.lock), "--manual-root", str(self.manual), "--json", "--inventory"])
        self.assertEqual(code, 0)
        data = json.loads(out.getvalue())
        ids = {row["id"] for row in data["entries"]}
        self.assertEqual(ids, {"a-main", "a-dialog", "b-main", "manual-shot"})
        self.assertEqual(data["inventory"]["total"]["references"], 3)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            check.main(["--gpgfrontend", str(self.gf), "--manifest", str(self.manifest), "--lock",
                        str(self.lock), "--manual-root", str(self.manual), "--json"])
        self.assertIsInstance(json.loads(out.getvalue()), list)
