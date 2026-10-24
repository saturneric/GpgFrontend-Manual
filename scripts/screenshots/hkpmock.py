"""A local stand-in for a key server, for the key server screenshots.

The application is told to reach ``http://keys.example.org`` through an HTTP
proxy; this is that proxy. It answers the HKP requests GpgFrontend makes
(``/pks/lookup`` with ``op=index`` and ``op=get``, ``/pks/add``) from the
demo keys in ``resource/screenshot/keyserver``, and refuses every other host,
so nothing leaves the machine. It listens on the loopback interface only.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlsplit

HOST = "keys.example.org"
PROXY_ENV = "GF_SCREENSHOT_KEYSERVER_PROXY"


@dataclass
class DemoKey:
    fingerprint: str
    algo: str
    length: str
    created: str
    expires: str
    uids: list[str] = field(default_factory=list)
    armored: bytes = b""

    def matches(self, search: str) -> bool:
        if search.lower().startswith("0x"):
            handle = search[2:].upper()
            return bool(handle) and self.fingerprint.endswith(handle)
        needle = search.lower()
        return any(needle in uid.lower() for uid in self.uids)


def load_keys(directory: Path) -> list[DemoKey]:
    """The demo keys, from gpg's --with-colons listing and their exports."""
    keys: list[DemoKey] = []
    listing = (directory / "listing.colons").read_text(encoding="utf-8")
    current: DemoKey | None = None
    for line in listing.splitlines():
        parts = line.split(":")
        if parts[0] == "pub":
            current = DemoKey("", parts[3], parts[2], parts[5], parts[6])
            keys.append(current)
        elif parts[0] == "fpr" and current is not None and not current.fingerprint:
            current.fingerprint = parts[9]
        elif parts[0] == "uid" and current is not None:
            current.uids.append(parts[9])
    for key in keys:
        key.armored = (directory / f"{key.fingerprint}.asc").read_bytes()
    return keys


def index_answer(keys: list[DemoKey], search: str) -> bytes:
    """A machine-readable HKP index (draft-shaw-openpgp-hkp, section 5.2)."""
    found = [k for k in keys if k.matches(search)]
    lines = [f"info:1:{len(found)}"]
    for key in found:
        lines.append(f"pub:{key.fingerprint}:{key.algo}:{key.length}:{key.created}:{key.expires}:")
        for uid in key.uids:
            lines.append(f"uid:{quote(uid, safe=' @<>().')}:{key.created}::")
    return ("\n".join(lines) + "\n").encode("utf-8")


class MockKeyServer:
    """The proxy, in a background thread for as long as the renderer runs."""

    def __init__(self, directory: Path) -> None:
        self.keys = load_keys(directory)
        self.requests: list[str] = []
        server = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: object) -> None:  # quiet
                pass

            def _target(self) -> tuple[str, str, dict[str, list[str]]]:
                url = urlsplit(self.path)
                host = (url.hostname or self.headers.get("Host", "").split(":")[0]).lower()
                return host, url.path, parse_qs(url.query)

            def _reply(self, code: int, body: bytes, kind: str = "text/plain") -> None:
                self.send_response(code)
                self.send_header("Content-Type", kind)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self) -> None:
                host, path, query = self._target()
                server.requests.append(f"GET {host}{path}")
                if host != HOST or path != "/pks/lookup":
                    self._reply(403, b"only the demo key server is served here\n")
                    return
                op = query.get("op", [""])[0]
                search = query.get("search", [""])[0]
                if op == "index":
                    self._reply(200, index_answer(server.keys, search))
                    return
                if op == "get":
                    found = [k for k in server.keys if k.matches(search)]
                    if found:
                        self._reply(200, found[0].armored, "application/pgp-keys")
                        return
                self._reply(404, b"no such key\n")

            def do_POST(self) -> None:
                host, path, _ = self._target()
                server.requests.append(f"POST {host}{path}")
                self.rfile.read(int(self.headers.get("Content-Length") or 0))
                if host == HOST and path == "/pks/add":
                    self._reply(200, b"Key added\n")
                    return
                self._reply(403, b"only the demo key server is served here\n")

            def do_CONNECT(self) -> None:
                server.requests.append(f"CONNECT {self.path}")
                self._reply(403, b"no tunnels\n")

        self._httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._httpd.daemon_threads = True
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()

    @property
    def address(self) -> str:
        host, port = self._httpd.server_address[:2]
        return f"{host}:{port}"

    def close(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
