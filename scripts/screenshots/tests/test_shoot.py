from __future__ import annotations

import hashlib
import io
import shutil
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from helpers import commit_change, git, make_gf_repo, short_tempdir, write

import fonts
import manifest
import shoot


class SyncSourceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = short_tempdir("gfsh")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.upstream = make_gf_repo(self.tmp / "upstream")
        quiet = mock.patch.object(shoot, "say")
        quiet.start()
        self.addCleanup(quiet.stop)
        self.clone = self.tmp / "clone"

    def test_clones_when_missing(self) -> None:
        head = shoot.sync_source(self.clone, "main", str(self.upstream), update=True)
        self.assertEqual(head, git(self.upstream, "rev-parse", "HEAD"))
        self.assertEqual(git(self.clone, "config", "core.autocrlf"), "false")

    def test_fast_forwards_an_existing_clone(self) -> None:
        shoot.sync_source(self.clone, "main", str(self.upstream), update=True)
        new = commit_change(self.upstream, "src/ui/main/MainWindow.cpp")
        self.assertEqual(shoot.sync_source(self.clone, "main", str(self.upstream), update=True), new)

    def test_no_update_leaves_the_clone_alone(self) -> None:
        old = shoot.sync_source(self.clone, "main", str(self.upstream), update=True)
        commit_change(self.upstream, "src/ui/main/MainWindow.cpp")
        self.assertEqual(shoot.sync_source(self.clone, "main", str(self.upstream), update=False), old)

    def test_refuses_local_changes(self) -> None:
        shoot.sync_source(self.clone, "main", str(self.upstream), update=True)
        write(self.clone / "README", "edited\n")
        with self.assertRaisesRegex(shoot.ShootError, "uncommitted changes"):
            shoot.sync_source(self.clone, "main", str(self.upstream), update=True)

    def test_untracked_files_do_not_block(self) -> None:
        shoot.sync_source(self.clone, "main", str(self.upstream), update=True)
        write(self.clone / "build" / "out.txt", "x\n")
        shoot.sync_source(self.clone, "main", str(self.upstream), update=True)

    def test_refuses_another_branch(self) -> None:
        shoot.sync_source(self.clone, "main", str(self.upstream), update=True)
        git(self.clone, "checkout", "-q", "-b", "feature")
        with self.assertRaisesRegex(shoot.ShootError, "on feature, not main"):
            shoot.sync_source(self.clone, "main", str(self.upstream), update=True)

    def test_refuses_a_non_empty_non_clone(self) -> None:
        write(self.clone / "stuff.txt", "x\n")
        with self.assertRaisesRegex(shoot.ShootError, "not a git clone"):
            shoot.sync_source(self.clone, "main", str(self.upstream), update=True)

    def test_no_update_never_clones(self) -> None:
        with self.assertRaisesRegex(shoot.ShootError, "--no-update"):
            shoot.sync_source(self.clone, "main", str(self.upstream), update=False)


class ArgvTest(unittest.TestCase):
    def parse(self, *argv: str):
        own, extra = shoot.split_passthrough(list(argv))
        return shoot.build_parser().parse_args(own), extra

    def test_dry_run(self) -> None:
        args, extra = self.parse("--binary", "gf.exe")
        self.assertEqual(shoot.run_py_argv(args, Path("src"), Path("gf.exe"), extra),
                         ["--gpgfrontend", "src", "--binary", "gf.exe"])

    def test_options_and_passthrough(self) -> None:
        args, extra = self.parse("--only", "a,b", "--force", "--repeat", "2", "--upload",
                                 "--", "--accept-baseline", "a")
        self.assertEqual(shoot.run_py_argv(args, Path("src"), Path("gf"), extra),
                         ["--gpgfrontend", "src", "--binary", "gf", "--only", "a,b", "--force",
                          "--repeat", "2", "--upload", "--accept-baseline", "a"])

    def test_recover(self) -> None:
        args, extra = self.parse("--recover", "--", "--resolve", "t1", "--retry-upload")
        self.assertEqual(shoot.run_py_argv(args, None, None, extra),
                         ["--recover", "--resolve", "t1", "--retry-upload"])

    def test_modes_are_exclusive(self) -> None:
        with self.assertRaises(SystemExit), mock.patch("sys.stderr", io.StringIO()):
            shoot.build_parser().parse_args(["--apply", "--upload"])


class FontPackageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = short_tempdir("gfsf")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_registry_names_resolve_the_manifest_families(self) -> None:
        values = [(name, f"C:\\fonts\\{Path(member).name}")
                  for pkg in shoot.FONT_PACKAGES for member, name in pkg.members.items()]
        self.assertEqual(fonts.match_registry("Noto Sans", values), "C:\\fonts\\NotoSans-Regular.ttf")
        self.assertEqual(fonts.match_registry("Noto Sans CJK SC", values),
                         "C:\\fonts\\NotoSansCJKsc-Regular.otf")

    def test_noto_sans_names(self) -> None:
        names = set(shoot._noto_sans_members().values())
        self.assertEqual(len(names), 18)
        for expected in ("Noto Sans Regular (TrueType)", "Noto Sans Italic (TrueType)",
                         "Noto Sans Bold Italic (TrueType)", "Noto Sans SemiBold (TrueType)"):
            self.assertIn(expected, names)

    def make_zip(self) -> tuple[Path, shoot.FontPackage]:
        archive = self.tmp / "pkg.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.writestr("dir/A-Regular.ttf", b"regular")
            zf.writestr("dir/A-Bold.ttf", b"bold")
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        pkg = shoot.FontPackage("A", archive.as_uri(), digest,
                                {"dir/A-Regular.ttf": "A Regular (TrueType)"})
        return archive, pkg

    def test_fetch_verifies_and_extracts(self) -> None:
        _, pkg = self.make_zip()
        with mock.patch("sys.stdout", io.StringIO()):
            got = shoot.fetch_package(pkg, self.tmp / "cache")
        files = shoot.extract_members(got, pkg, self.tmp / "files")
        self.assertEqual([(p.name, n) for p, n in files], [("A-Regular.ttf", "A Regular (TrueType)")])
        self.assertEqual(files[0][0].read_bytes(), b"regular")

    def test_fetch_rejects_a_wrong_hash(self) -> None:
        _, pkg = self.make_zip()
        bad = shoot.FontPackage(pkg.family, pkg.url, "0" * 64, pkg.members)
        with mock.patch("sys.stdout", io.StringIO()), self.assertRaisesRegex(shoot.ShootError, "sha256"):
            shoot.fetch_package(bad, self.tmp / "cache")
        self.assertFalse((self.tmp / "cache" / "pkg.zip").exists())


class PipelineFilesTest(unittest.TestCase):
    def test_helper_is_not_part_of_inputs_hash(self) -> None:
        tmp = short_tempdir("gfsp")
        self.addCleanup(shutil.rmtree, tmp, True)
        write(tmp / "run.py", "x\n")
        write(tmp / "shoot.py", "y\n")
        self.assertEqual(set(manifest.pipeline_files(tmp)), {"run.py"})


class MainTest(unittest.TestCase):
    def test_missing_binary_is_reported(self) -> None:
        err = io.StringIO()
        with mock.patch.object(shoot, "in_venv", return_value=True), \
                mock.patch.dict("os.environ", {shoot.BINARY_ENV: ""}), mock.patch("sys.stderr", err):
            self.assertEqual(shoot.main([]), 2)
        self.assertIn("--binary", err.getvalue())

    def test_upload_needs_credentials(self) -> None:
        tmp = short_tempdir("gfsm")
        self.addCleanup(shutil.rmtree, tmp, True)
        binary = write(tmp / "gf.exe", "")
        err = io.StringIO()
        env = {name: "" for name in shoot.CDN_ENVS}
        with mock.patch.object(shoot, "in_venv", return_value=True), \
                mock.patch.dict("os.environ", env), mock.patch("sys.stderr", err):
            self.assertEqual(shoot.main(["--binary", str(binary), "--upload"]), 2)
        self.assertIn("GF_MANUAL_CDN_API", err.getvalue())


if __name__ == "__main__":
    unittest.main()
