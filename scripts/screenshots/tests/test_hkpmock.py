"""The local mock key server: what it answers, and that it answers nothing else."""

from __future__ import annotations

import shutil
import unittest
import urllib.error
import urllib.request

from helpers import short_tempdir, write

import hkpmock

LISTING = """\
tru::1:1743508800:0:3:1:5
pub:-:255:22:F32819327EBEC29F:1735732800:::-:::scSC::::::23::0:
fpr:::::::::3818A814A0DE75F628AF39C9F32819327EBEC29F:
uid:-::::1735732800::ABC::Grace Example <grace@example.org>::::::::::0:
sub:-:255:18:AAAA:1735732800::::::e::::::23:
fpr:::::::::1111111111111111111111111111111111111111:
"""


class MockKeyServerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = short_tempdir("gfhkp")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        write(self.tmp / "listing.colons", LISTING)
        write(self.tmp / "3818A814A0DE75F628AF39C9F32819327EBEC29F.asc", "ARMORED\n")
        self.server = hkpmock.MockKeyServer(self.tmp)
        self.addCleanup(self.server.close)
        proxy = urllib.request.ProxyHandler({"http": "http://" + self.server.address})
        self.opener = urllib.request.build_opener(proxy)

    def get(self, url: str) -> tuple[int, bytes]:
        try:
            with self.opener.open(url, timeout=5) as reply:
                return reply.status, reply.read()
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read()

    def test_index_lists_matching_keys_with_their_primary_fingerprint(self) -> None:
        code, body = self.get("http://keys.example.org/pks/lookup?search=grace%40example.org&op=index&options=mr")
        self.assertEqual(code, 200)
        self.assertEqual(body.decode().splitlines(), [
            "info:1:1",
            "pub:3818A814A0DE75F628AF39C9F32819327EBEC29F:22:255:1735732800::",
            "uid:Grace Example <grace@example.org>:1735732800::",
        ])
        code, body = self.get("http://keys.example.org/pks/lookup?search=nobody%40example.org&op=index")
        self.assertEqual(body.decode().splitlines(), ["info:1:0"])

    def test_get_by_key_id_or_fingerprint(self) -> None:
        for handle in ("0xF32819327EBEC29F", "0x3818A814A0DE75F628AF39C9F32819327EBEC29F"):
            self.assertEqual(self.get(f"http://keys.example.org/pks/lookup?search={handle}&op=get"),
                             (200, b"ARMORED\n"))
        self.assertEqual(self.get("http://keys.example.org/pks/lookup?search=0xDEAD&op=get")[0], 404)

    def test_other_hosts_are_refused_and_nothing_is_forwarded(self) -> None:
        self.assertEqual(self.get("http://example.com/pks/lookup?search=a&op=index")[0], 403)
        self.assertEqual(self.get("http://keys.example.org/other")[0], 403)
        self.assertEqual(self.server.requests[-2:], ["GET example.com/pks/lookup", "GET keys.example.org/other"])


if __name__ == "__main__":
    unittest.main()
