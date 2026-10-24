from __future__ import annotations

import json
import os

from PIL import Image

from helpers import World, commit_change, write


class RunWorld(World):
    def publish_all(self) -> None:
        """Brings every renderable entry to a committed lock + baseline."""
        self.start_cdn()
        code, out, err = self.run_pipeline("--upload")
        self.assertEqual(code, 0, out + err)
        self.assertEqual(set(self.statuses().values()), {"updated"})

    def rendered_ids(self, log) -> list[str]:
        ids = []
        for line in log.read_text().splitlines():
            if "--screenshot " in line:
                out = line.split("--out ")[1].split(" ")[0]
                ids.append(os.path.basename(out).rsplit(".", 1)[0])
        return ids


class SelectionTest(RunWorld):
    def test_unknown_or_manual_only_id_is_usage_error(self) -> None:
        self.assertEqual(self.run_pipeline("--only", "nope")[0], 2)
        self.assertEqual(self.run_pipeline("--only", "manual-shot")[0], 2)
        self.assertFalse((self.cache / "last-run.json").exists())

    def test_replace_without_upload_is_would_replace(self) -> None:
        code, out, err = self.run_pipeline()
        self.assertEqual(code, 0, out + err)
        self.assertEqual(self.statuses(), {"a-main": "would-replace", "a-dialog": "would-replace",
                                           "b-main": "would-replace"})
        self.assertTrue((self.cache / "preview" / "a-main.webp").exists())
        self.assertEqual(self.read_lock(), {})

    def test_force_with_and_without_only(self) -> None:
        self.publish_all()
        log = self.tmp / "calls.log"
        self.set_fake({"log": str(log)})
        self.assertEqual(self.run_pipeline()[0], 0)
        self.assertEqual(set(self.statuses().values()), {"unchanged"})
        self.assertEqual(self.rendered_ids(log), [])
        self.assertEqual(self.run_pipeline("--force")[0], 0)
        self.assertEqual(sorted(self.rendered_ids(log)), ["a-dialog", "a-main", "b-main"])
        log.write_text("")
        self.assertEqual(self.run_pipeline("--force", "--only", "a-main")[0], 0)
        self.assertEqual(self.rendered_ids(log), ["a-main"])
        self.assertEqual(list(self.statuses()), ["a-main"])

    def test_override_validation(self) -> None:
        self.publish_all()
        # Valid baseline: accept-baseline does not apply.
        code, _, err = self.run_pipeline("--force", "--accept-baseline", "a-main")
        self.assertEqual(code, 2)
        self.assertIn("--force-replace", err)
        code, _, err = self.run_pipeline("--force", "--accept-baseline", "a-main", "--force-replace", "a-main")
        self.assertEqual(code, 2)
        # Not stale, so not selected without --force.
        code, _, err = self.run_pipeline("--force-replace", "a-main")
        self.assertEqual(code, 2)
        self.assertIn("not selected", err)
        code, out, err = self.run_pipeline("--force", "--force-replace", "a-main")
        self.assertEqual(code, 0, out + err)
        self.assertEqual(self.statuses()["a-main"], "would-replace")
        self.assertEqual(self.statuses()["b-main"], "unchanged")

    def test_scenario_missing_from_binary_is_usage_error(self) -> None:
        log = self.tmp / "calls.log"
        self.set_fake({"log": str(log)})
        self.manifest.write_text(self.manifest.read_text().replace(
            "scenario: key-generate-dialog", "scenario: no-such-scenario"))
        code, _, err = self.run_pipeline()
        self.assertEqual(code, 2)
        self.assertIn("no-such-scenario", err)
        self.assertEqual(self.rendered_ids(log), [])

    def test_recover_rejects_selection_flags(self) -> None:
        for extra in (["--only", "a-main"], ["--force"], ["--accept-baseline", "a-main"],
                      ["--force-replace", "a-main"], ["--repeat", "2"]):
            self.assertEqual(self.recover(*extra)[0], 2, extra)
        self.assertEqual(self.run_pipeline("--resolve", "x", "--url", "https://a/b")[0], 2)


class DirtyRuleTest(RunWorld):
    def test_dirty_without_allow_is_refused_and_not_rendered(self) -> None:
        log = self.tmp / "calls.log"
        self.set_fake({"log": str(log)})
        write(self.gf / "src/ui/main/MainWindow.cpp", "dirty\n")
        code, _, _ = self.run_pipeline()
        self.assertEqual(code, 1)
        self.assertEqual(self.statuses()["a-main"], "refused-dirty")
        self.assertEqual(self.statuses()["b-main"], "would-replace")
        self.assertNotIn("a-main", self.rendered_ids(log))

    def test_dirty_with_allow_is_preview_only(self) -> None:
        write(self.gf / "src/ui/main/MainWindow.cpp", "dirty\n")
        code, _, _ = self.run_pipeline("--allow-dirty")
        self.assertEqual(code, 0)
        self.assertEqual(self.statuses()["a-main"], "preview-only-dirty")
        self.assertTrue((self.cache / "preview" / "a-main.png").exists())

    def test_dirty_with_upload_never_publishes_but_clean_entries_do(self) -> None:
        cdn = self.start_cdn()
        before = self.doc("a.md")
        write(self.gf / "src/ui/main/MainWindow.cpp", "dirty\n")
        code, out, err = self.run_pipeline("--allow-dirty", "--upload")
        self.assertEqual(code, 1, out + err)
        st = self.statuses()
        self.assertEqual(st["a-main"], "preview-only-dirty")
        self.assertEqual(st["a-dialog"], "updated")
        self.assertEqual(st["b-main"], "updated")
        self.assertEqual(len(cdn.requests), 2)
        lock = self.read_lock()
        self.assertNotIn("a-main", lock)
        self.assertIn("https://cdn.example.org/i/a1.webp", self.doc("a.md").decode())
        self.assertNotEqual(self.doc("a.md"), before)  # img-2 was updated
        self.assertFalse((self.cache / "baseline" / "a-main.png").exists())

    def test_platform_mismatch_is_preview_only_under_upload(self) -> None:
        cdn = self.start_cdn()
        self.set_fake({"platform_name": "xcb", "product": "Debian GNU/Linux 13"})
        code, _, _ = self.run_pipeline("--upload")
        self.assertEqual(code, 1)
        self.assertEqual(set(self.statuses().values()), {"preview-only-platform"})
        self.assertEqual(cdn.requests, [])
        self.assertEqual(self.read_lock(), {})


class DiffTest(RunWorld):
    def test_missing_baseline_then_accept_baseline(self) -> None:
        self.publish_all()
        (self.cache / "baseline" / "a-main.png").unlink()
        commit_change(self.gf, "src/ui/main/MainWindow.cpp")
        code, _, _ = self.run_pipeline("--only", "a-main")
        self.assertEqual(code, 1)
        self.assertEqual(self.statuses()["a-main"], "baseline-unavailable")
        code, out, err = self.run_pipeline("--only", "a-main", "--accept-baseline", "a-main", "--upload")
        self.assertEqual(code, 0, out + err)
        self.assertEqual(self.statuses()["a-main"], "updated")

    def test_baseline_sha_mismatch_is_unavailable(self) -> None:
        self.publish_all()
        Image.new("RGBA", (10, 10), (1, 2, 3, 255)).save(self.cache / "baseline" / "a-main.png")
        commit_change(self.gf, "src/ui/main/MainWindow.cpp")
        self.run_pipeline("--only", "a-main")
        self.assertEqual(self.statuses()["a-main"], "baseline-unavailable")

    def test_sub_threshold_advances_lock_then_ok(self) -> None:
        self.publish_all()
        old = self.read_lock()["a-main"]
        self.set_fake({"tweak_pixels": 5})
        new_head = commit_change(self.gf, "src/ui/main/MainWindow.cpp")
        self.assertEqual(self.check_rows(binary=True)["a-main"], ["outdated"])
        self.run_pipeline("--only", "a-main")
        self.assertEqual(self.statuses()["a-main"], "unchanged-lock-not-advanced")
        self.assertEqual(self.read_lock()["a-main"], old)
        code, out, err = self.run_pipeline("--only", "a-main", "--apply")
        self.assertEqual(code, 0, out + err)
        self.assertEqual(self.statuses()["a-main"], "lock-advanced")
        new = self.read_lock()["a-main"]
        self.assertEqual(new["gpgfrontend_commit"], new_head)
        for key in ("url", "webp_sha256", "pixels_sha256"):
            self.assertEqual(new[key], old[key])
        self.assertEqual(self.check_rows(binary=True)["a-main"], ["ok"])

    def test_emptied_link_is_restored_from_the_lock(self) -> None:
        self.publish_all()
        url = self.read_lock()["a-main"]["url"]
        page = self.manual / "src" / "content" / "docs" / "guides" / "a.md"
        page.write_bytes(page.read_bytes().replace(f"[img-1]: {url}".encode(), b"[img-1]: TODO"))
        self.assertEqual(self.check_rows(binary=True)["a-main"], ["missing"])

        self.run_pipeline("--only", "a-main")
        self.assertEqual(self.statuses()["a-main"], "would-restore-doc")
        self.assertIn(b"[img-1]: TODO", self.doc("a.md"))

        code, out, err = self.run_pipeline("--only", "a-main", "--apply")
        self.assertEqual(code, 0, out + err)
        self.assertEqual(self.statuses()["a-main"], "doc-restored")
        self.assertIn(f"[img-1]: {url}".encode(), self.doc("a.md"))
        self.assertEqual(self.check_rows(binary=True)["a-main"], ["ok"])

    def test_large_change_is_replace(self) -> None:
        self.publish_all()
        self.set_fake({"variant": 40})
        commit_change(self.gf, "src/ui/main/MainWindow.cpp")
        self.run_pipeline("--only", "a-main")
        self.assertEqual(self.statuses()["a-main"], "would-replace")


class UploadOutcomeTest(RunWorld):
    def test_success_request_shape(self) -> None:
        cdn = self.start_cdn()
        self.run_pipeline("--only", "a-main", "--upload")
        self.assertEqual(len(cdn.requests), 1)
        req = cdn.requests[0]
        self.assertTrue(req["has_image"] and req["has_token"])
        self.assertTrue(req["content_type"].startswith("multipart/form-data"))
        self.assertIn("https://img.example.org/i/up1.webp", self.doc("a.md").decode())

    def _expect_failed(self, mode: str) -> None:
        cdn = self.start_cdn()
        cdn.mode = mode
        before = self.doc("a.md")
        code, _, _ = self.run_pipeline("--only", "a-main", "--upload")
        self.assertEqual(code, 1)
        self.assertEqual(self.statuses()["a-main"], "failed:upload-failed")
        self.assertEqual(self.doc("a.md"), before)
        self.assertEqual(self.read_lock(), {})

    def test_error_json_is_upload_failed(self) -> None:
        self._expect_failed("error")

    def test_http_500_is_upload_failed(self) -> None:
        self._expect_failed("http500")

    def test_dropped_connection_is_upload_unknown(self) -> None:
        cdn = self.start_cdn()
        cdn.mode = "drop"
        code, _, _ = self.run_pipeline("--only", "a-main", "--upload")
        self.assertEqual(code, 3)
        self.assertEqual(self.statuses()["a-main"], "upload-unknown")
        # A later normal run does not upload the entry again.
        cdn.mode = "success"
        code, _, _ = self.run_pipeline("--only", "a-main", "--upload")
        self.assertEqual(code, 3)
        self.assertEqual(len(cdn.requests), 1)

    def test_upload_needs_credentials(self) -> None:
        self.assertEqual(self.run_pipeline("--upload")[0], 2)


class MiscRunTest(RunWorld):
    def test_stale_binary_mtime_warns_without_blocking(self) -> None:
        os.utime(self.binary, (946684800, 946684800))
        code, out, _ = self.run_pipeline("--only", "a-main")
        self.assertEqual(code, 0)
        self.assertEqual(self.statuses()["a-main"], "would-replace")
        self.assertTrue(any("older than" in w for w in self.last_run()["warnings"]))
        self.assertIn("warning:", out)

    def test_repeat_identical_and_mismatch(self) -> None:
        self.assertEqual(self.run_pipeline("--only", "a-main", "--repeat", "2")[0], 0)
        self.set_fake({"nondeterministic": True})
        self.assertEqual(self.run_pipeline("--only", "a-main", "--repeat", "2")[0], 1)
        self.assertEqual(self.statuses()["a-main"], "failed:repeat-mismatch")

    def test_footprint_outside_throwaway_fails(self) -> None:
        self.set_fake({"write_appdata": str(self.appdata / "GpgFrontendLeak"), "write_appdata_render_only": True})
        self.assertEqual(self.run_pipeline("--only", "a-main")[0], 1)
        self.assertEqual(self.statuses()["a-main"], "failed:footprint")

    def test_footprint_in_probe_fails(self) -> None:
        self.set_fake({"write_appdata": str(self.appdata / "GpgFrontendLeak")})
        self.assertEqual(self.run_pipeline("--only", "a-main")[0], 1)
        self.assertEqual(self.statuses()["a-main"], "failed:env-probe")
        self.assertIn("footprint", json.dumps(self.last_run()))

    def test_gate_failure_in_probe(self) -> None:
        self.set_fake({"gate_failures": ["font:Noto Sans"]})
        self.assertEqual(self.run_pipeline("--only", "a-main")[0], 1)
        self.assertEqual(self.statuses()["a-main"], "failed:env-probe")
        self.assertIn("font:Noto Sans", json.dumps(self.last_run()))

    def test_missing_highlight_fails_entry(self) -> None:
        self.set_fake({"missing": ["InfoBoardWidget"]})
        self.run_pipeline("--only", "a-main")
        self.assertEqual(self.statuses()["a-main"], "failed:highlight-missing")

    def test_command_line_follows_contract(self) -> None:
        log = self.tmp / "calls.log"
        self.set_fake({"log": str(log)})
        self.run_pipeline("--only", "a-main")
        lines = log.read_text().splitlines()
        probe = next(l for l in lines if "--screenshot-env" in l)
        render = next(l for l in lines if "--screenshot main-window" in l)
        for line in (probe, render):
            self.assertTrue(line.startswith("--temp-profile"))
            for flag in ("--locale en_US", "--theme light", "--size 160x100", "--clock 2026-01-15T10:00:00Z",
                         "--demo-gnupghome", "--fixtures", "--out", "--timeout 30000"):
                self.assertIn(flag, line)
        self.assertIn("demo-gnupghome", render)
