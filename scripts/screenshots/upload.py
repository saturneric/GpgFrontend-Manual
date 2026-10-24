"""EasyImages 2.0 upload: POST multipart `image` + `token` to $GF_MANUAL_CDN_API.

A successful response is JSON {result, code, url, srcName, thumb, del}.
The token is read from $GF_MANUAL_CDN_TOKEN and is never stored.
"""

from __future__ import annotations

import ipaddress
import json
import os
import secrets
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

from common import UsageError

API_ENV = "GF_MANUAL_CDN_API"
TOKEN_ENV = "GF_MANUAL_CDN_TOKEN"
TIMEOUT_S = 120


class UploadFailed(Exception):
    """The server answered and did not store the image; a retry is safe."""

    def __init__(self, reason: str, raw: str = "") -> None:
        super().__init__(reason)
        self.reason = reason
        self.raw = raw


class UploadUnknown(Exception):
    """The request may have reached the server; the outcome is unknown."""


@dataclass
class Uploaded:
    url: str
    del_url: Optional[str]
    raw: str


@dataclass
class Credentials:
    api: str
    token: str

    @property
    def host(self) -> str:
        return urlparse(self.api).hostname or ""


def _is_loopback(host: str) -> bool:
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def is_https_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and bool(parsed.hostname) and not any(c.isspace() for c in url)


def credentials_from_env() -> Credentials:
    api = os.environ.get(API_ENV, "").strip()
    token = os.environ.get(TOKEN_ENV, "").strip()
    if not api or not token:
        raise UsageError(f"--upload needs {API_ENV} and {TOKEN_ENV}")
    parsed = urlparse(api)
    if parsed.scheme != "https" and not (parsed.scheme == "http" and _is_loopback(parsed.hostname or "")):
        raise UsageError(f"{API_ENV} must be an https URL")
    return Credentials(api, token)


def _multipart(fields: dict[str, str], file_field: str, filename: str, data: bytes,
               content_type: str) -> tuple[bytes, str]:
    boundary = "----gfshot" + secrets.token_hex(16)
    parts: list[bytes] = []
    for name, value in fields.items():
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode("utf-8"))
    parts.append(
        (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{file_field}\"; filename=\"{filename}\"\r\n"
         f"Content-Type: {content_type}\r\n\r\n").encode("utf-8") + data + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def parse_response(raw: str) -> Uploaded:
    try:
        data: Any = json.loads(raw)
    except ValueError as exc:
        raise UploadFailed("response is not JSON", raw) from exc
    if not isinstance(data, dict) or data.get("result") != "success":
        message = data.get("message") or data.get("result") if isinstance(data, dict) else None
        raise UploadFailed(f"server rejected the upload: {message or 'no success result'}", raw)
    url = data.get("url")
    if not isinstance(url, str) or not is_https_url(url):
        raise UploadFailed(f"response url is not https: {url!r}", raw)
    del_url = data.get("del") if isinstance(data.get("del"), str) else None
    return Uploaded(url=url, del_url=del_url, raw=raw)


def upload_file(creds: Credentials, path: Path, filename: str) -> Uploaded:
    body, content_type = _multipart({"token": creds.token}, "image", filename, Path(path).read_bytes(), "image/webp")
    request = urllib.request.Request(creds.api, data=body, method="POST",
                                     headers={"Content-Type": content_type, "Accept": "application/json"})
    handlers = [urllib.request.ProxyHandler({})] if _is_loopback(creds.host) else []
    opener = urllib.request.build_opener(*handlers)
    try:
        with opener.open(request, timeout=TIMEOUT_S) as response:
            raw = response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace") if exc.fp else ""
        raise UploadFailed(f"HTTP {exc.code}", raw) from exc
    except urllib.error.URLError as exc:
        if isinstance(exc.reason, (ConnectionRefusedError, socket.gaierror)):
            raise UploadFailed(f"connection failed before sending: {exc.reason}") from exc
        raise UploadUnknown(str(exc.reason)) from exc
    except (OSError, TimeoutError) as exc:
        raise UploadUnknown(str(exc)) from exc
    return parse_response(raw)
