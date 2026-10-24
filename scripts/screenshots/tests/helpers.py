"""Shared fixtures: a temp GpgFrontend git repo, a temp manual tree, a fake
binary and a localhost EasyImages mock. Nothing here touches the network
beyond 127.0.0.1."""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Optional
from unittest import mock

PIPELINE_DIR = Path(__file__).resolve().parents[1]
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

FAKE_SCRIPT = Path(__file__).resolve().parent / "fakegf.py"

PAGE_A = """---
title: Page A
---

Intro text.

![Main window][img-1]

Some steps.

   ![][img-2]

[img-1]: https://cdn.example.org/i/a1.webp
[img-2]:
  https://cdn.example.org/i/a2.webp
[link]: https://example.org/
"""

PAGE_B = "# B\r\n\r\n![][img-1]\r\n\r\nText line.\r\n\r\n[img-1]: https://cdn.example.org/i/b1.webp\r\n"

MANIFEST = """
defaults:
  platform: windows11
  size: 160x100
  fonts: ["Noto Sans"]
  frame: {radius: 4, shadow: 4, padding: 8}
global_sources: [src/screenshot/, resource/screenshot/]
entries:
  - id: a-main
    doc: src/content/docs/guides/a.md
    ref: img-1
    scenario: main-window
    sources: [src/ui/main/]
    highlight: InfoBoardWidget
  - id: a-dialog
    doc: src/content/docs/guides/a.md
    ref: img-2
    scenario: key-generate-dialog
    sources: [src/ui/dialog/]
    highlight: {name: nameEdit, style: arrow}
  - id: b-main
    doc: src/content/docs/guides/b.md
    ref: img-1
    scenario: main-window
    sources: [src/ui/other/]
  - id: manual-shot
    doc: src/content/docs/guides/b.md
    ref: img-9
    status: manual-only
"""


def git(repo: Path, *args: str) -> str:
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.org",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.org")
    out = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True, env=env)
    return out.stdout.decode().strip()


def write(path: Path, text: str, newline_exact: bool = True) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def make_gf_repo(root: Path) -> Path:
    root.mkdir(parents=True)
    git(root, "init", "-q", "-b", "main")
    for rel in ("src/screenshot/Mode.cpp", "resource/screenshot/demo-gnupghome/pubring.kbx",
                "resource/screenshot/fixtures/decrypt-verify.asc", "src/ui/main/MainWindow.cpp",
                "src/ui/dialog/Dialog.cpp", "src/ui/other/Other.cpp", "README"):
        write(root / rel, f"// {rel}\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "init")
    return root


def commit_change(repo: Path, rel: str, text: str = "change\n") -> str:
    write(repo / rel, text)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", f"edit {rel}")
    return git(repo, "rev-parse", "HEAD")


def make_fake_binary(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        launcher = directory / "fakegf.cmd"
        launcher.write_text(f'@"{sys.executable}" "{FAKE_SCRIPT}" %*\r\n', encoding="utf-8")
    else:
        launcher = directory / "fakegf"
        launcher.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{FAKE_SCRIPT}" "$@"\n', encoding="utf-8")
        launcher.chmod(0o755)
    return launcher


class MockCdn:
    """EasyImages-like endpoint on 127.0.0.1. Modes: success, error, http500, drop."""

    def __init__(self) -> None:
        self.mode = "success"
        self.requests: list[dict[str, Any]] = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: Any) -> None:
                pass

            def do_POST(self) -> None:  # noqa: N802
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length)
                n = len(outer.requests) + 1
                outer.requests.append({
                    "has_image": b'name="image"' in body and b"RIFF" in body,
                    "has_token": b'name="token"\r\n\r\nsecret-token' in body,
                    "content_type": self.headers.get("Content-Type", ""),
                })
                if outer.mode == "drop":
                    self.close_connection = True
                    self.connection.shutdown(2)
                    return
                if outer.mode == "http500":
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b"internal error")
                    return
                if outer.mode == "error":
                    payload = {"result": "failed", "code": 202, "message": "token invalid"}
                else:
                    payload = {"result": "success", "code": 200,
                               "url": f"https://img.example.org/i/up{n}.webp", "srcName": "x.webp",
                               "thumb": f"https://img.example.org/thumb/up{n}.webp",
                               "del": f"https://img.example.org/del/secret{n}"}
                data = json.dumps(payload).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.server.server_address[1]}/api/index.php"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()


def short_tempdir(prefix: str) -> Path:
    base = "/tmp" if os.name != "nt" else None
    return Path(tempfile.mkdtemp(prefix=prefix, dir=base))


class World(unittest.TestCase):
    """A complete temp setup; subclasses get self.gf, self.manual, ... ready."""

    crlf_b = True

    def setUp(self) -> None:
        self.tmp = short_tempdir("gfst")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.gf = make_gf_repo(self.tmp / "gf")
        self.manual = self.tmp / "manual"
        docs = self.manual / "src" / "content" / "docs" / "guides"
        write(docs / "a.md", PAGE_A)
        write(docs / "b.md", PAGE_B)
        self.scripts = self.manual / "scripts" / "screenshots"
        self.manifest = write(self.scripts / "screenshots.yaml", MANIFEST)
        self.lock = write(self.scripts / "screenshots.lock.json", "{}\n")
        self.cache = self.scripts / ".screenshots-cache"
        self.binary = make_fake_binary(self.tmp / "bin")
        self.fake_config_path = self.tmp / "fake.json"
        self.appdata = self.tmp / "appdata"
        self.appdata.mkdir()
        self.work_root = self.tmp / "w"
        self.cdn: Optional[MockCdn] = None
        self.set_fake({})
        env = {
            "FAKEGF_CONFIG": str(self.fake_config_path),
            "GF_SHOTS_NO_XVFB": "1",
            "GF_SHOTS_APPDATA_ROOTS": str(self.appdata),
            "GF_MANUAL_CDN_API": "",
            "GF_MANUAL_CDN_TOKEN": "",
            "GF_SCREENSHOT_BINARY": "",
        }
        patcher = mock.patch.dict(os.environ, env)
        patcher.start()
        self.addCleanup(patcher.stop)

    # Helpers ---------------------------------------------------------------

    def set_fake(self, cfg: dict[str, Any]) -> None:
        self.fake_config_path.write_text(json.dumps(cfg), encoding="utf-8")

    def start_cdn(self) -> MockCdn:
        self.cdn = MockCdn()
        self.addCleanup(self.cdn.close)
        os.environ["GF_MANUAL_CDN_API"] = self.cdn.url
        os.environ["GF_MANUAL_CDN_TOKEN"] = "secret-token"
        return self.cdn

    def common_args(self, binary: bool = True) -> list[str]:
        args = ["--gpgfrontend", str(self.gf), "--manifest", str(self.manifest), "--lock", str(self.lock),
                "--cache", str(self.cache), "--manual-root", str(self.manual), "--work-root", str(self.work_root)]
        if binary:
            args += ["--binary", str(self.binary)]
        return args

    def run_pipeline(self, *args: str, binary: bool = True) -> tuple[int, str, str]:
        import run

        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = run.main(self.common_args(binary) + list(args))
        return code, out.getvalue(), err.getvalue()

    def recover(self, *args: str) -> tuple[int, str, str]:
        import run

        out, err = io.StringIO(), io.StringIO()
        base = ["--recover", "--manifest", str(self.manifest), "--lock", str(self.lock), "--cache",
                str(self.cache), "--manual-root", str(self.manual)]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = run.main(base + list(args))
        return code, out.getvalue(), err.getvalue()

    def last_run(self) -> dict[str, Any]:
        return json.loads((self.cache / "last-run.json").read_text(encoding="utf-8"))

    def statuses(self) -> dict[str, str]:
        return {e["id"]: e["status"] for e in self.last_run()["entries"]}

    def read_lock(self) -> dict[str, Any]:
        return json.loads(self.lock.read_text(encoding="utf-8"))

    def doc(self, name: str) -> bytes:
        return (self.manual / "src" / "content" / "docs" / "guides" / name).read_bytes()

    def check_rows(self, binary: bool = False, pipeline_dir: Optional[Path] = None) -> dict[str, list[str]]:
        import check
        from apply import read_lock
        from manifest import load_manifest
        from render import RenderConfig, Renderer

        renderer = Renderer(RenderConfig(self.binary, self.gf, self.work_root)) if binary else None
        ctx = check.CheckContext(load_manifest(self.manifest), read_lock(self.lock), self.manual, self.gf,
                                 renderer, pipeline_dir or PIPELINE_DIR)
        rows, _ = check.compute(ctx)
        return {(r.id or f"{r.doc}#{r.ref}"): r.statuses for r in rows}
