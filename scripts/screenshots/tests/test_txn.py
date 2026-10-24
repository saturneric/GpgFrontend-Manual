from __future__ import annotations

import json
import os

from helpers import World

import txn as txnmod


class TxnWorld(World):
    def setUp(self) -> None:
        super().setUp()
        self.cdn_server = self.start_cdn()

    def crash_at(self, state: str, entry: str = "a-main") -> dict:
        os.environ[txnmod.CRASH_ENV] = state
        try:
            with self.assertRaises(txnmod.InjectedCrash):
                self.run_pipeline("--only", entry, "--upload")
        finally:
            del os.environ[txnmod.CRASH_ENV]
        return self.txn_data()

    def txn_dirs(self) -> list:
        root = self.cache / "txn"
        return sorted(p for p in root.iterdir() if p.is_dir()) if root.exists() else []

    def txn_data(self, index: int = -1) -> dict:
        return json.loads((self.txn_dirs()[index] / "txn.json").read_text(encoding="utf-8"))

    def a_url(self) -> str:
        return "https://img.example.org/i/up1.webp"


class CrashRecoveryTest(TxnWorld):
    def test_prepared_becomes_abandoned(self) -> None:
        before = self.doc("a.md")
        self.assertEqual(self.crash_at("prepared")["state"], "prepared")
        code, out, _ = self.recover()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.txn_data()["state"], "abandoned")
        self.assertEqual(self.cdn_server.requests, [])
        self.assertEqual(self.doc("a.md"), before)
        self.assertEqual(self.read_lock(), {})
        # The entry is still stale and the next run picks it up.
        code, _, _ = self.run_pipeline("--only", "a-main", "--upload")
        self.assertEqual(code, 0)
        self.assertEqual(self.statuses()["a-main"], "updated")

    def test_uploading_becomes_unknown_then_resolve_url(self) -> None:
        data = self.crash_at("uploading")
        code, out, _ = self.recover()
        self.assertEqual(code, 3)
        self.assertEqual(self.txn_data()["state"], "upload-unknown")
        # Never retried automatically.
        self.assertEqual(self.recover()[0], 3)
        self.assertEqual(self.cdn_server.requests, [])
        manual_url = "https://img.example.org/i/found-in-admin.webp"
        code, out, err = self.recover("--resolve", data["txn_id"], "--url", manual_url)
        self.assertEqual(code, 0, out + err)
        final = self.txn_data()
        self.assertEqual(final["state"], "committed")
        self.assertEqual(final["upload"]["del"], txnmod.DEL_UNKNOWN)
        self.assertIn(manual_url, self.doc("a.md").decode())
        self.assertEqual(self.read_lock()["a-main"]["url"], manual_url)
        self.assertTrue((self.cache / "baseline" / "a-main.png").exists())

    def test_uploading_resolve_retry_upload(self) -> None:
        data = self.crash_at("uploading")
        self.recover()
        code, out, err = self.recover("--resolve", data["txn_id"], "--retry-upload")
        self.assertEqual(code, 0, out + err)
        self.assertEqual(len(self.cdn_server.requests), 1)
        self.assertEqual(self.txn_data()["state"], "committed")
        self.assertIn(self.a_url(), self.doc("a.md").decode())

    def test_resolve_validation(self) -> None:
        data = self.crash_at("uploaded")
        self.assertEqual(self.recover("--resolve", data["txn_id"], "--url", "https://x/y")[0], 2)
        self.assertEqual(self.recover("--resolve", "nope", "--url", "https://x/y")[0], 2)
        self.assertEqual(self.recover("--resolve", data["txn_id"])[0], 2)

    def test_uploaded_completes_doc_lock_baseline(self) -> None:
        self.crash_at("uploaded")
        self.assertNotIn(self.a_url(), self.doc("a.md").decode())
        code, out, _ = self.recover()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.txn_data()["state"], "committed")
        self.assertIn(self.a_url(), self.doc("a.md").decode())
        self.assertEqual(self.read_lock()["a-main"]["url"], self.a_url())
        self.assertTrue((self.cache / "baseline" / "a-main.png").exists())
        self.assertEqual(len(self.cdn_server.requests), 1)

    def test_doc_applied_completes_lock_only(self) -> None:
        self.crash_at("doc-applied")
        doc_after_crash = self.doc("a.md")
        self.assertIn(self.a_url(), doc_after_crash.decode())
        self.assertEqual(self.read_lock(), {})
        self.recover()
        self.assertEqual(self.doc("a.md"), doc_after_crash)
        self.assertEqual(self.read_lock()["a-main"]["url"], self.a_url())
        self.assertEqual(self.txn_data()["state"], "committed")

    def test_lock_applied_completes_baseline_only(self) -> None:
        self.crash_at("lock-applied")
        lock = self.read_lock()
        self.assertFalse((self.cache / "baseline" / "a-main.png").exists())
        self.recover()
        self.assertEqual(self.read_lock(), lock)
        self.assertTrue((self.cache / "baseline" / "a-main.png").exists())
        self.assertEqual(self.txn_data()["state"], "committed")

    def test_tampered_webp_is_artifact_corrupt(self) -> None:
        self.crash_at("uploaded")
        before_doc, before_lock = self.doc("a.md"), self.read_lock()
        webp = self.txn_dirs()[-1] / "final.webp"
        webp.write_bytes(webp.read_bytes() + b"x")
        code, _, _ = self.recover()
        self.assertEqual(code, 3)
        self.assertEqual(self.txn_data()["state"], "artifact-corrupt")
        self.assertEqual(self.doc("a.md"), before_doc)
        self.assertEqual(self.read_lock(), before_lock)

    def test_lock_changed_after_prepare_is_conflict(self) -> None:
        self.crash_at("uploaded")
        foreign = {"a-main": {"url": "https://other/x.webp", "note": "newer data"}}
        self.lock.write_text(json.dumps(foreign), encoding="utf-8")
        before_doc = self.doc("a.md")
        code, out, _ = self.recover()
        self.assertEqual(code, 3)
        self.assertEqual(self.txn_data()["state"], "conflict")
        self.assertEqual(self.read_lock(), foreign)
        self.assertEqual(self.doc("a.md"), before_doc)
        self.assertIn("del:", out)


class DocEditTest(TxnWorld):
    def test_concurrent_unrelated_edit_is_kept(self) -> None:
        self.crash_at("uploaded")
        path = self.manual / "src/content/docs/guides/a.md"
        path.write_bytes(self.doc("a.md").replace(b"Some steps.", b"Some edited steps."))
        self.assertEqual(self.recover()[0], 0)
        text = self.doc("a.md").decode()
        self.assertIn("Some edited steps.", text)
        self.assertIn(f"[img-1]: {self.a_url()}", text)

    def test_edit_to_same_definition_is_conflict(self) -> None:
        self.crash_at("uploaded")
        path = self.manual / "src/content/docs/guides/a.md"
        edited = self.doc("a.md").replace(b"https://cdn.example.org/i/a1.webp", b"https://elsewhere/x.webp")
        path.write_bytes(edited)
        self.assertEqual(self.recover()[0], 3)
        self.assertEqual(self.txn_data()["state"], "conflict")
        self.assertEqual(self.doc("a.md"), edited)
        self.assertEqual(self.read_lock(), {})

    def test_crlf_doc_keeps_crlf(self) -> None:
        code, _, _ = self.run_pipeline("--only", "b-main", "--upload")
        self.assertEqual(code, 0)
        raw = self.doc("b.md")
        self.assertIn(b"https://img.example.org/i/up1.webp\r\n", raw)
        self.assertEqual(raw.count(b"\n"), raw.count(b"\r\n"))

    def test_del_never_in_committed_files(self) -> None:
        code, _, _ = self.run_pipeline("--upload")
        self.assertEqual(code, 0)
        for path in (self.lock, self.manual / "src/content/docs/guides/a.md",
                     self.manual / "src/content/docs/guides/b.md", self.cache / "last-run.json"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("/del/", text, path)
            self.assertNotIn('"del"', text, path)
        # It is kept in the ignored transaction cache.
        self.assertIn("/del/secret", (self.txn_dirs()[0] / "txn.json").read_text(encoding="utf-8"))

    def test_conflict_stops_remaining_transactions(self) -> None:
        import apply

        original = apply.apply_doc

        def conflicting(*args, **kwargs):
            raise apply.Conflict("simulated concurrent edit")

        txnmod.apply_doc = conflicting
        try:
            code, out, _ = self.run_pipeline("--upload")
        finally:
            txnmod.apply_doc = original
        self.assertEqual(code, 3)
        st = self.statuses()
        self.assertEqual(st["a-main"], "conflict")
        self.assertEqual(st["a-dialog"], "failed:stopped-after-conflict")
        self.assertEqual(len(self.cdn_server.requests), 1)
        self.assertIn("del: https://img.example.org/del/secret1", out)
