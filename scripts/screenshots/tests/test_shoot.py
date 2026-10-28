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


class DemoDataTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = short_tempdir("gfsd")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        base = self.tmp / "resource" / "screenshot"
        write(base / "demo-gnupghome" / "pubring.kbx", "x")
        write(base / "demo-gnupghome" / "private-keys-v1.d" / "A.key", "x")
        write(base / "fixtures" / "decrypt-verify.asc", "x")
        write(base / "keyserver" / "listing.colons", "x")
        self.base = base

    def test_complete_demo_data_passes(self) -> None:
        self.assertEqual(shoot.missing_demo_data(self.tmp), [])
        shoot.check_demo_data(self.tmp)

    def test_missing_secret_keys_are_named(self) -> None:
        shutil.rmtree(self.base / "demo-gnupghome" / "private-keys-v1.d")
        (self.base / "demo-gnupghome" / "private-keys-v1.d").mkdir()  # present but empty
        with self.assertRaisesRegex(shoot.ShootError, "demo secret keys"):
            shoot.check_demo_data(self.tmp)

    def test_missing_key_server_data_is_named(self) -> None:
        (self.base / "keyserver" / "listing.colons").unlink()
        self.assertEqual(len(shoot.missing_demo_data(self.tmp)), 1)
        self.assertIn("key server", shoot.missing_demo_data(self.tmp)[0])


class Sized:
    def __init__(self, size, fonts=("Noto Sans",)) -> None:
        self.size = size
        self.fonts = fonts


class DisplayTest(unittest.TestCase):
    def test_largest_fixed_size_ignores_auto(self) -> None:
        entries = [Sized((1280, 960)), Sized((1200, 760)), Sized(None), Sized((900, 1000))]
        self.assertEqual(shoot.largest_size(entries), (1280, 1000))
        self.assertIsNone(shoot.largest_size([Sized(None)]))

    def test_4k_at_200_percent_fits(self) -> None:
        # 3840x2160 with a 72 px taskbar
        self.assertEqual(shoot.display_problem((1280, 960), (3840, 2088)), "")

    def test_small_display_is_reported(self) -> None:
        problem = shoot.display_problem((1280, 960), (2560, 1528))
        self.assertIn("2592x2016", problem)
        self.assertIn("2560x1528", problem)

    def test_families_are_collected_once_in_order(self) -> None:
        entries = [Sized(None, ("Noto Sans", "Noto Sans CJK SC")), Sized(None, ("Noto Sans",))]
        self.assertEqual(shoot.manifest_families(entries), ["Noto Sans", "Noto Sans CJK SC"])

    def test_only_narrows_the_selection(self) -> None:
        every = shoot.selected_entries(None)
        one = shoot.selected_entries(every[0].id)
        self.assertEqual([e.id for e in one], [every[0].id])
        self.assertTrue(all(e.renderable for e in every))


class PipelineFilesTest(unittest.TestCase):
    def test_helper_is_not_part_of_inputs_hash(self) -> None:
        tmp = short_tempdir("gfsp")
        self.addCleanup(shutil.rmtree, tmp, True)
        write(tmp / "run.py", "x\n")
        write(tmp / "shoot.py", "y\n")
        self.assertEqual(set(manifest.pipeline_files(tmp)), {"run.py"})


class DefaultPathsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = short_tempdir("gfsd")
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_default_source_is_gpgfrontend_next_to_the_manual(self) -> None:
        with mock.patch.dict("os.environ", {shoot.SOURCE_ENV: ""}):
            self.assertEqual(shoot.default_source(), shoot.MANUAL_ROOT.parent / "GpgFrontend")

    def test_default_portable_dir_is_next_to_the_manual(self) -> None:
        self.assertEqual(shoot.default_portable_dir(), shoot.MANUAL_ROOT.parent / "GpgFrontend Portable")

    def test_portable_binary_finds_the_bundled_exe(self) -> None:
        exe = write(self.tmp / "bin" / "GpgFrontend.exe", "")
        with mock.patch.object(shoot.os, "name", "nt"):
            self.assertEqual(shoot.portable_binary(self.tmp), exe)
        self.assertIsNone(shoot.portable_binary(self.tmp / "missing"))

    def test_portable_binary_finds_an_appimage(self) -> None:
        app = write(self.tmp / "GpgFrontend-abc-linux-x86_64-portable.AppImage", "")
        with mock.patch.object(shoot.os, "name", "posix"):
            self.assertEqual(shoot.portable_binary(self.tmp), app)

    def test_resolve_binary_falls_back_to_the_portable_bundle(self) -> None:
        exe = write(self.tmp / "bin" / "GpgFrontend.exe", "")
        args = shoot.build_parser().parse_args([])
        with mock.patch.dict("os.environ", {shoot.BINARY_ENV: ""}), \
                mock.patch.object(shoot, "default_portable_dir", return_value=self.tmp), \
                mock.patch.object(shoot.os, "name", "nt"):
            self.assertEqual(shoot.resolve_binary(args), exe.resolve())

    def test_resolve_binary_accepts_the_bundle_folder(self) -> None:
        exe = write(self.tmp / "bin" / "GpgFrontend.exe", "")
        args = shoot.build_parser().parse_args(["--binary", str(self.tmp)])
        with mock.patch.object(shoot.os, "name", "nt"):
            self.assertEqual(shoot.resolve_binary(args), exe.resolve())
        empty = self.tmp / "empty"
        empty.mkdir()
        args = shoot.build_parser().parse_args(["--binary", str(empty)])
        with self.assertRaises(shoot.ShootError):
            shoot.resolve_binary(args)


class MainTest(unittest.TestCase):
    def test_missing_binary_is_reported(self) -> None:
        tmp = short_tempdir("gfsm")
        self.addCleanup(shutil.rmtree, tmp, True)
        err = io.StringIO()
        with mock.patch.object(shoot, "in_venv", return_value=True), \
                mock.patch.object(shoot, "default_portable_dir", return_value=tmp / "GpgFrontend Portable"), \
                mock.patch.dict("os.environ", {shoot.BINARY_ENV: ""}), mock.patch("sys.stderr", err):
            self.assertEqual(shoot.main([]), 2)
        self.assertIn("--binary", err.getvalue())
        self.assertIn("GpgFrontend Portable", err.getvalue())

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
