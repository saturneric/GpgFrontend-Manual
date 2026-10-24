#!/usr/bin/env python3
"""One command for the whole screenshot job.

    py -3 shoot.py --binary <path>\\GpgFrontend.exe            # dry run
    py -3 shoot.py --binary <path>\\GpgFrontend.exe --apply    # write lock and docs
    py -3 shoot.py --binary <path>\\GpgFrontend.exe --upload   # also upload to the CDN

Steps, each stopping with a message when it cannot go on:

1. Creates `.venv` and installs requirements.txt (again when it changes), then
   re-runs itself inside the venv.
2. Clones the GpgFrontend repository, or fast-forwards an existing clone. A
   clone with local changes, or on another branch, is left alone and the run
   stops; `--no-update` uses it as it is.
3. Checks that every font family in the manifest resolves. On Windows,
   `--install-fonts` downloads the pinned Noto releases, verifies them and
   installs them for the current user (no admin rights needed).
4. Refuses to start while another GpgFrontend is running: its writes to the
   per-user app data would fail the footprint check.
5. Runs run.py with the options given here, plus anything after `--`.

This helper only prepares and calls the pipeline. It is not part of
`inputs_hash`, and it never runs git in the Manual repository.

`--recover` skips steps 2-4 and runs `run.py --recover`.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parent
MANUAL_ROOT = HERE.parent.parent
VENV = HERE / ".venv"
CACHE = HERE / ".screenshots-cache"
REQUIREMENTS = HERE / "requirements.txt"
REQ_MARKER = VENV / ".requirements.sha256"

REPO_URL = "https://github.com/saturneric/GpgFrontend.git"
DEFAULT_REF = "main"
SOURCE_ENV = "GF_SHOTS_GPGFRONTEND"
BINARY_ENV = "GF_SCREENSHOT_BINARY"
CDN_ENVS = ("GF_MANUAL_CDN_API", "GF_MANUAL_CDN_TOKEN")

_FONTS_KEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"


class ShootError(Exception):
    """A step cannot continue; the message says what to do."""


@dataclass(frozen=True)
class FontPackage:
    family: str
    url: str
    sha256: str
    # zip member -> registry value name, as Windows itself would register it
    members: dict[str, str]


def _noto_sans_members() -> dict[str, str]:
    weights = ["Thin", "ExtraLight", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Black"]
    out = {}
    for weight in weights:
        for italic in (False, True):
            if weight == "Regular":
                style = "Italic" if italic else "Regular"
            else:
                style = f"{weight}Italic" if italic else weight
            label = {"Regular": "Regular", "Italic": "Italic"}.get(style, style.replace("Italic", " Italic"))
            out[f"NotoSans/unhinted/ttf/NotoSans-{style}.ttf"] = f"Noto Sans {label} (TrueType)"
    return out


FONT_PACKAGES = (
    FontPackage(
        "Noto Sans",
        "https://github.com/notofonts/latin-greek-cyrillic/releases/download/NotoSans-v2.015/NotoSans-v2.015.zip",
        "0c34df072a3fa7efbb7cbf34950e1f971a4447cffe365d3a359e2d4089b958f5",
        _noto_sans_members(),
    ),
    FontPackage(
        "Noto Sans CJK SC",
        "https://github.com/notofonts/noto-cjk/releases/download/Sans2.004/08_NotoSansCJKsc.zip",
        "a927e56f53bd6c3b920bc139c0b94aa36c7d9ad0cf009b159437a1a003581140",
        {
            "NotoSansCJKsc-Regular.otf": "Noto Sans CJK SC (OpenType)",
            "NotoSansCJKsc-Medium.otf": "Noto Sans CJK SC Medium (OpenType)",
            "NotoSansCJKsc-Bold.otf": "Noto Sans CJK SC Bold (OpenType)",
        },
    ),
)


def say(msg: str) -> None:
    print(f"[shoot] {msg}", flush=True)


# --- arguments -----------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Prepare everything and run the manual screenshot pipeline.",
        epilog="Arguments after `--` go to run.py unchanged, e.g. -- --accept-baseline main-window",
    )
    p.add_argument("--binary", type=Path, help=f"screenshot-mode GpgFrontend binary (else ${BINARY_ENV})")
    p.add_argument("--gpgfrontend", type=Path,
                   help=f"GpgFrontend clone to create or update (else ${SOURCE_ENV}, "
                        "else GpgFrontend-Src next to the Manual repository)")
    p.add_argument("--ref", default=DEFAULT_REF, help="branch to clone and fast-forward (default: main)")
    p.add_argument("--repo-url", default=REPO_URL, help="where to clone GpgFrontend from")
    p.add_argument("--no-update", action="store_true", help="use the GpgFrontend clone as it is")
    p.add_argument("--install-fonts", action="store_true",
                   help="Windows: download and install missing Noto fonts for this user")
    p.add_argument("--ignore-running", action="store_true",
                   help="start even though another GpgFrontend is running")
    p.add_argument("--only", help="comma separated entry ids")
    p.add_argument("--force", action="store_true", help="render every entry, stale or not")
    p.add_argument("--repeat", type=int, help="render N times and require identical bytes")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="write lock, docs and cache (no network)")
    mode.add_argument("--upload", action="store_true", help="also upload replacements to the CDN")
    mode.add_argument("--recover", action="store_true", help="only finish pending transactions")
    return p


def split_passthrough(argv: list[str]) -> tuple[list[str], list[str]]:
    if "--" in argv:
        i = argv.index("--")
        return argv[:i], argv[i + 1:]
    return argv, []


def default_source() -> Path:
    env = os.environ.get(SOURCE_ENV)
    return Path(env) if env else MANUAL_ROOT.parent / "GpgFrontend-Src"


def run_py_argv(args: argparse.Namespace, source: Optional[Path], binary: Optional[Path],
                extra: list[str]) -> list[str]:
    if args.recover:
        return ["--recover", *extra]
    out = ["--gpgfrontend", str(source), "--binary", str(binary)]
    if args.only:
        out += ["--only", args.only]
    if args.force:
        out.append("--force")
    if args.repeat is not None:
        out += ["--repeat", str(args.repeat)]
    if args.apply:
        out.append("--apply")
    if args.upload:
        out.append("--upload")
    return out + extra


# --- 1. venv ---------------------------------------------------------------------


def venv_python(venv: Path = VENV) -> Path:
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def in_venv(venv: Path = VENV) -> bool:
    try:
        return Path(sys.prefix).resolve() == venv.resolve()
    except OSError:
        return False


def requirements_digest() -> str:
    return hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()


def ensure_venv() -> Path:
    py = venv_python()
    if not py.exists():
        say(f"creating {VENV}")
        subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)
    digest = requirements_digest()
    if not REQ_MARKER.exists() or REQ_MARKER.read_text(encoding="ascii").strip() != digest:
        say("installing requirements.txt")
        proc = subprocess.run([str(py), "-m", "pip", "install", "--disable-pip-version-check",
                               "-q", "-r", str(REQUIREMENTS)])
        if proc.returncode != 0:
            raise ShootError("pip install failed; check the network and run again")
        REQ_MARKER.write_text(digest + "\n", encoding="ascii")
    return py


# --- 2. GpgFrontend clone ----------------------------------------------------------


def _git(repo: Optional[Path], *args: str, check: bool = True) -> str:
    cmd = ["git", "-c", "core.quotepath=off"]
    if repo is not None:
        cmd += ["-C", str(repo)]
    try:
        proc = subprocess.run(cmd + list(args), capture_output=True, check=False)
    except OSError as exc:
        raise ShootError(f"cannot run git: {exc}") from exc
    if check and proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise ShootError(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout.decode("utf-8", "replace").strip()


def sync_source(path: Path, ref: str, url: str, update: bool) -> str:
    """Clones or fast-forwards `path` to `ref`; returns HEAD."""
    if not (path / ".git").exists():
        if path.exists() and any(path.iterdir()):
            raise ShootError(f"{path} exists, is not empty and is not a git clone; "
                             "pass --gpgfrontend with another path")
        if not update:
            raise ShootError(f"{path} is not a GpgFrontend clone, and --no-update forbids cloning")
        say(f"cloning {url} ({ref}) into {path}")
        # Demo data must stay byte-identical; resource/screenshot/.gitattributes
        # also says so, this keeps the rest of the tree as committed too.
        _git(None, "clone", "--config", "core.autocrlf=false", "--branch", ref, url, str(path))
        return _git(path, "rev-parse", "HEAD")

    head = _git(path, "rev-parse", "HEAD")
    if not update:
        say(f"using {path} as it is ({head[:12]})")
        return head
    changed = _git(path, "status", "--porcelain", "--untracked-files=no")
    if changed:
        raise ShootError(f"{path} has uncommitted changes; commit or stash them, "
                         "or pass --no-update to render from it as it is")
    branch = _git(path, "symbolic-ref", "--short", "-q", "HEAD", check=False)
    if branch != ref:
        raise ShootError(f"{path} is on {branch or 'a detached HEAD'}, not {ref}; "
                         f"check out {ref}, pass --ref {branch or '<branch>'}, or pass --no-update")
    say(f"updating {path} ({ref})")
    _git(path, "fetch", "--quiet", "origin", ref)
    _git(path, "merge", "--ff-only", "--quiet", "FETCH_HEAD")
    new = _git(path, "rev-parse", "HEAD")
    if new != head:
        say(f"{head[:12]} -> {new[:12]}")
    return new


# --- 3. fonts --------------------------------------------------------------------


def manifest_families() -> list[str]:
    from manifest import load_manifest  # needs the venv (PyYAML)

    families: list[str] = []
    for entry in load_manifest(HERE / "screenshots.yaml").entries:
        if entry.renderable:
            for family in entry.fonts:
                if family not in families:
                    families.append(family)
    return families


def missing_fonts(families: list[str]) -> list[str]:
    import fonts

    return [f for f in families if fonts.resolve_font_file(f) is None]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_package(pkg: FontPackage, cache: Path) -> Path:
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / pkg.url.rsplit("/", 1)[1]
    if target.exists() and _sha256_file(target) == pkg.sha256:
        return target
    say(f"downloading {pkg.url}")
    tmp = target.with_suffix(".part")
    with urllib.request.urlopen(pkg.url, timeout=120) as resp, tmp.open("wb") as out:  # noqa: S310
        shutil.copyfileobj(resp, out)
    actual = _sha256_file(tmp)
    if actual != pkg.sha256:
        tmp.unlink()
        raise ShootError(f"{pkg.url}: sha256 {actual} does not match the pinned {pkg.sha256}")
    os.replace(tmp, target)
    return target


def extract_members(archive: Path, pkg: FontPackage, dest: Path) -> list[tuple[Path, str]]:
    dest.mkdir(parents=True, exist_ok=True)
    out = []
    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
        for member, reg_name in pkg.members.items():
            if member not in names:
                raise ShootError(f"{archive.name} has no {member}")
            path = dest / Path(member).name
            path.write_bytes(zf.read(member))
            out.append((path, reg_name))
    return out


def install_user_fonts(files: list[tuple[Path, str]]) -> None:  # pragma: no cover - Windows only
    import ctypes
    import winreg

    dest = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts"
    dest.mkdir(parents=True, exist_ok=True)
    gdi32 = ctypes.windll.gdi32
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, _FONTS_KEY) as key:
        for src, reg_name in files:
            target = dest / src.name
            shutil.copyfile(src, target)
            winreg.SetValueEx(key, reg_name, 0, winreg.REG_SZ, str(target))
            # Loaded into this session now; the registry entry loads it at sign-in.
            if gdi32.AddFontResourceW(str(target)) == 0:
                say(f"  {src.name}: AddFontResource failed; it loads at the next sign-in")
            say(f"  installed {src.name}")
    hwnd_broadcast, wm_fontchange, smto_abortifhung = 0xFFFF, 0x001D, 0x0002
    ctypes.windll.user32.SendMessageTimeoutW(hwnd_broadcast, wm_fontchange, 0, 0,
                                             smto_abortifhung, 1000, None)


def ensure_fonts(install: bool) -> None:
    if os.name != "nt":
        return  # Linux previews: the binary's own font gate reports by name
    missing = missing_fonts(manifest_families())
    if not missing:
        return
    packages = {p.family: p for p in FONT_PACKAGES}
    unknown = [f for f in missing if f not in packages]
    if unknown:
        raise ShootError(f"font(s) not installed and not installable by this helper: {', '.join(unknown)}")
    if not install:
        raise ShootError(f"font(s) not installed: {', '.join(missing)}. Install them, "
                         "or pass --install-fonts to install the pinned Noto releases for this user")
    for family in missing:
        pkg = packages[family]
        archive = fetch_package(pkg, CACHE / "fonts")
        install_user_fonts(extract_members(archive, pkg, CACHE / "fonts" / "files"))
    still = missing_fonts(manifest_families())
    if still:
        raise ShootError(f"font(s) still not resolved after installing: {', '.join(still)}")


# --- 4. running GpgFrontend --------------------------------------------------------


def running_gpgfrontend() -> list[str]:
    """Names of running processes that look like GpgFrontend."""
    found: list[str] = []
    if os.name == "nt":
        proc = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, check=False)
        for line in proc.stdout.decode("utf-8", "replace").splitlines():
            name = line.split('","', 1)[0].strip('"')
            if name.lower() == "gpgfrontend.exe":
                found.append(name)
    else:
        for comm in Path("/proc").glob("[0-9]*/comm"):
            try:
                name = comm.read_text().strip()
            except OSError:
                continue
            if name.lower() == "gpgfrontend":
                found.append(name)
    return found


# --- main ------------------------------------------------------------------------


def resolve_binary(args: argparse.Namespace) -> Path:
    binary = args.binary or (Path(os.environ[BINARY_ENV]) if os.environ.get(BINARY_ENV) else None)
    if binary is None:
        raise ShootError(f"--binary or ${BINARY_ENV} is required")
    if not binary.is_file():
        raise ShootError(f"binary not found: {binary}")
    return binary.resolve()


def explain(code: int, args: argparse.Namespace) -> None:
    if args.recover:
        return
    if code == 0 and not (args.apply or args.upload):
        say(f"dry run done; previews in {CACHE / 'preview'}")
    elif code == 0:
        say("done; review the doc and lock changes with git diff before committing")
    elif code == 1:
        say(f"an entry failed or was refused; details in {CACHE / 'last-run.json'}")
    elif code == 3:
        say("a transaction needs a decision; run: shoot.py --recover")


def main(argv: Optional[list[str]] = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    own, extra = split_passthrough(raw)
    args = build_parser().parse_args(own)
    try:
        if not in_venv():
            py = ensure_venv()
            return subprocess.run([str(py), str(Path(__file__).resolve()), *raw]).returncode

        sys.path.insert(0, str(HERE))
        if args.recover:
            source, binary = None, None
        else:
            binary = resolve_binary(args)
            if args.upload:
                unset = [name for name in CDN_ENVS if not os.environ.get(name)]
                if unset:
                    raise ShootError(f"--upload needs {', '.join(unset)} set")
            source = (args.gpgfrontend or default_source()).resolve()
            sync_source(source, args.ref, args.repo_url, update=not args.no_update)
            ensure_fonts(args.install_fonts)
            running = running_gpgfrontend()
            if running and not args.ignore_running:
                raise ShootError("GpgFrontend is running; close it first (its app data writes would "
                                 "fail the footprint check), or pass --ignore-running")
        cmd = [sys.executable, str(HERE / "run.py"), *run_py_argv(args, source, binary, extra)]
        code = subprocess.run(cmd, cwd=str(HERE)).returncode
        explain(code, args)
        return code
    except ShootError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
