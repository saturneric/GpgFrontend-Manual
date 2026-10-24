"""Runs the GpgFrontend screenshot mode in an isolated throwaway environment.

Both the render (`--screenshot <scenario>`) and the environment probe
(`--screenshot-env`) are built from the same resolved manifest entry and run
with the same subprocess environment, so their env records are comparable.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from PIL import Image

import envhash
import fonts
import gitutil
from common import (DEFAULT_CACHE, DEFAULT_MANIFEST, PipelineError, UsageError, canonical_json,
                    load_json, split_ids)
from manifest import Entry, Manifest, load_manifest

XVFB_SCREEN = "-screen 0 2560x1600x24"
EXIT_REASONS = {
    2: "usage-or-precondition",
    3: "timeout",
    4: "output-unwritable",
    5: "unexpected-modal",
    6: "environment-gate",
}
CAPTURE_MODES = ("window", "dialog", "composite")
TIMEOUT_MARGIN_S = 60
# Unix sockets are limited to 108 bytes. The demo homedir ends up at
# $XDG_DATA_HOME/BKTUS/<AppProfileName>/profiles/.tmp-<16hex>/db and gpg-agent
# puts S.gpg-agent.browser inside it.
_SOCKET_LIMIT = 107
_SOCKET_TAIL = "/BKTUS/GpgFrontendXXXXXXXXXXXX/profiles/.tmp-0123456789abcdef/db/S.gpg-agent.browser"
# Paths that must not leak from the parent environment into a render.
_SCRUB_ENV = (
    "GNUPGHOME", "QT_SCALE_FACTOR", "QT_SCREEN_SCALE_FACTORS", "QT_AUTO_SCREEN_SCALE_FACTOR",
    "QT_SCALE_FACTOR_ROUNDING_POLICY", "QT_ENABLE_HIGHDPI_SCALING", "QT_FONT_DPI",
    "QT_QPA_PLATFORM", "QT_STYLE_OVERRIDE", "QT_QPA_PLATFORMTHEME",
)
APPDATA_ROOTS_ENV = "GF_SHOTS_APPDATA_ROOTS"
# Where GpgFrontend creates a temporary profile's tree (core/profile).
SESSION_STORAGE_ENV = "GF_PROFILE_PACKAGE_STORAGE_DIR"
NO_XVFB_ENV = "GF_SHOTS_NO_XVFB"


def default_work_root() -> Path:
    # Fixed and free of the user's name: on Windows the temporary profile
    # lives under TEMP, which points in here, and the settings page shows
    # that path. A per-user %TEMP% would put the account name into the manual.
    if os.name == "nt":
        drive = os.environ.get("SystemDrive") or "C:"
        return Path(drive + "\\") / "gf-shot"
    return Path(f"/tmp/gf-shot-{os.getuid()}")


def fresh_session_base() -> Optional[Path]:
    """Linux: the memory-backed folder the temporary profile is created in,
    emptied first.

    The profile has the same name on every run, so the folder it lands in must
    be one the pipeline owns and empties: a session a crash left in the
    application's own default folder could not be found again (its pointer
    lived in the throwaway directory) and would stand in the next run's way.
    On Windows the session is made under TEMP, which already points into the
    throwaway directory.
    """
    shm = Path("/dev/shm")
    if os.name == "nt" or not shm.is_dir():
        return None
    base = shm / f"gf-shot-{os.getuid()}"
    if base.is_symlink() or (base.exists() and base.stat().st_uid != os.getuid()):
        raise PipelineError(f"{base} is a symlink or not owned by this user")
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(mode=0o700)
    return base


def default_xvfb_cmd() -> list[str]:
    """xvfb-run on Linux. GF_SHOTS_NO_XVFB=1 runs without it (fake binaries in
    tests); such renders get a non-reference platform tag."""
    if os.environ.get(NO_XVFB_ENV) == "1":
        return []
    if sys.platform.startswith("linux"):
        return ["xvfb-run", "-a", "-s", XVFB_SCREEN]
    return []


def real_appdata_roots() -> list[Path]:
    """Where a real (non-ephemeral) GpgFrontend profile would write."""
    override = os.environ.get(APPDATA_ROOTS_ENV)
    if override is not None:
        return [Path(p) for p in override.split(os.pathsep) if p]
    if os.name == "nt":
        return [Path(os.environ[v]) / "BKTUS" for v in ("LOCALAPPDATA", "APPDATA") if os.environ.get(v)]
    home = Path.home()
    return [
        Path(os.environ.get("XDG_DATA_HOME") or home / ".local" / "share") / "BKTUS",
        Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config") / "BKTUS",
        Path(os.environ.get("XDG_STATE_HOME") or home / ".local" / "state") / "BKTUS",
        Path(os.environ.get("XDG_CACHE_HOME") or home / ".cache") / "BKTUS",
        home / "Library" / "Application Support" / "BKTUS",
    ]


def footprint_snapshot(roots: list[Path]) -> set[str]:
    """Every path under <root>/GpgFrontend* for each root."""
    seen: set[str] = set()
    for root in roots:
        if not root.is_dir():
            continue
        for child in root.iterdir():
            if not child.name.startswith("GpgFrontend"):
                continue
            seen.add(str(child))
            if child.is_dir():
                for dirpath, dirnames, filenames in os.walk(child):
                    for name in dirnames + filenames:
                        seen.add(os.path.join(dirpath, name))
    return seen


@dataclass
class EnvInfo:
    record: dict[str, Any]
    core_hash: str
    env_hash: str
    platform: str
    font_files: list[dict[str, Any]]

    def lock_env(self) -> dict[str, Any]:
        env = envhash.strip_volatile(self.record)
        env["platform"] = self.platform
        env["font_files"] = self.font_files
        return env


@dataclass
class RunOutcome:
    ok: bool
    exit_code: Optional[int]
    reason: str = ""
    detail: str = ""
    env: Optional[EnvInfo] = None
    png: Optional[Path] = None
    json_path: Optional[Path] = None
    geometry: Optional[dict[str, Any]] = None
    footprint: list[str] = field(default_factory=list)

    @property
    def failure(self) -> str:
        return f"{self.reason}: {self.detail}" if self.detail else self.reason


@dataclass
class RenderConfig:
    binary: Path
    gpgfrontend: Path
    work_root: Optional[Path] = None
    keep_work: bool = False
    xvfb_cmd: Optional[list[str]] = None
    appdata_roots: Optional[list[Path]] = None
    font_resolver: fonts.FontResolver = fonts.resolve_font_file

    def resolved_xvfb(self) -> list[str]:
        return default_xvfb_cmd() if self.xvfb_cmd is None else list(self.xvfb_cmd)


class Renderer:
    def __init__(self, cfg: RenderConfig) -> None:
        self.cfg = cfg
        self.binary = Path(cfg.binary)
        if not self.binary.is_file():
            raise UsageError(f"binary not found: {self.binary}")
        self.work_root = Path(cfg.work_root) if cfg.work_root else default_work_root()
        self.xvfb = cfg.resolved_xvfb()
        if self.xvfb and not shutil.which(self.xvfb[0]):
            raise UsageError(f"{self.xvfb[0]} not found; it is needed for Linux previews")
        self._font_cache: dict[str, dict] = {}
        self._probe_cache: dict[tuple, RunOutcome] = {}

    # Paths -----------------------------------------------------------------

    def demo_gnupghome(self) -> Path:
        return Path(self.cfg.gpgfrontend) / "resource" / "screenshot" / "demo-gnupghome"

    def fixtures(self) -> Path:
        return Path(self.cfg.gpgfrontend) / "resource" / "screenshot" / "fixtures"

    def _prepare_root(self) -> None:
        root = self.work_root
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        if os.name != "nt":
            st = os.lstat(root)
            if os.path.islink(root) or st.st_uid != os.getuid():
                raise PipelineError(f"work root {root} is a symlink or not owned by this user")
            if len(str(root)) + 4 + len(_SOCKET_TAIL) > _SOCKET_LIMIT:
                raise UsageError(
                    f"work root {root} is too long: the gpg-agent socket path would exceed "
                    f"{_SOCKET_LIMIT} bytes. Use a shorter --work-root.")

    def _new_workdir(self) -> Path:
        """One fixed directory, emptied first: the application shows paths
        under it, so its name must be the same on every run. Renders run one
        at a time; two pipelines sharing a work root would collide."""
        self._prepare_root()
        candidate = self.work_root / "run"
        if candidate.is_symlink():
            raise PipelineError(f"{candidate} is a symlink; refusing to use it")
        if candidate.exists():
            shutil.rmtree(candidate)
        candidate.mkdir(mode=0o700)
        return candidate

    def subprocess_env(self, work: Path) -> dict[str, str]:
        env = {k: v for k, v in os.environ.items() if k not in _SCRUB_ENV}
        env["TZ"] = "UTC"
        if os.name == "nt":
            layout = {"LOCALAPPDATA": "la", "APPDATA": "ra", "TEMP": "t", "TMP": "t", "USERPROFILE": "alice"}
        else:
            layout = {"HOME": "alice", "XDG_DATA_HOME": "d", "XDG_CONFIG_HOME": "c",
                      "XDG_STATE_HOME": "s", "XDG_CACHE_HOME": "k", "TMPDIR": "t"}
        for var, sub in layout.items():
            path = work / sub
            path.mkdir(exist_ok=True)
            env[var] = str(path)
        session = fresh_session_base()
        if session is not None:
            env[SESSION_STORAGE_ENV] = str(session)
        return env

    # Command lines -----------------------------------------------------------

    def command(self, entry: Entry, out: Path, probe: bool) -> list[str]:
        mode = ["--screenshot-env"] if probe else ["--screenshot", entry.scenario or ""]
        cmd = [
            str(self.binary), "--temp-profile", *mode,
            "--locale", entry.locale,
            "--theme", entry.theme,
            "--font-family", ",".join(entry.fonts),
            *(["--size", entry.size_str] if entry.size is not None else []),
            "--clock", entry.clock,
            "--demo-gnupghome", str(self.demo_gnupghome()),
            "--fixtures", str(self.fixtures()),
            "--out", str(out),
            "--timeout", str(entry.timeout_ms),
        ]
        return self.xvfb + cmd

    def list_scenarios(self) -> dict[str, dict[str, str]]:
        work = self._new_workdir()
        try:
            proc = subprocess.run(
                self.xvfb + [str(self.binary), "--screenshot-list"],
                env=self.subprocess_env(work), capture_output=True, timeout=120, check=False,
            )
        finally:
            self._cleanup(work)
        if proc.returncode != 0:
            raise PipelineError(f"--screenshot-list exited {proc.returncode}: "
                                f"{proc.stderr.decode('utf-8', 'replace').strip()[-400:]}")
        scenarios = {}
        for line in proc.stdout.decode("utf-8", "replace").splitlines():
            parts = line.strip().split("\t")
            if len(parts) == 3:
                scenarios[parts[0]] = {"size": parts[1], "capture_mode": parts[2]}
        return scenarios

    # Running -----------------------------------------------------------------

    def _cleanup(self, work: Path) -> None:
        if not self.cfg.keep_work:
            shutil.rmtree(work, ignore_errors=True)

    def _run(self, entry: Entry, probe: bool, dest_dir: Optional[Path], stem: str) -> RunOutcome:
        work = self._new_workdir()
        out_dir = work / "o"
        out_dir.mkdir()
        out = out_dir / (f"{stem}.json" if probe else f"{stem}.png")
        json_path = out.with_suffix(".json")
        roots = self.cfg.appdata_roots if self.cfg.appdata_roots is not None else real_appdata_roots()
        before = footprint_snapshot(roots)
        try:
            try:
                proc = subprocess.run(
                    self.command(entry, out, probe), env=self.subprocess_env(work),
                    capture_output=True, timeout=entry.timeout_ms / 1000 + TIMEOUT_MARGIN_S, check=False,
                )
                code: Optional[int] = proc.returncode
                stderr = proc.stderr.decode("utf-8", "replace").strip()
            except subprocess.TimeoutExpired:
                code, stderr = None, "the binary did not exit; killed by the runner"
            except OSError as exc:
                return RunOutcome(False, None, "launch-failed", str(exc))
            new = sorted(footprint_snapshot(roots) - before)
            outcome = self._evaluate(entry, probe, code, stderr, out, json_path)
            outcome.footprint = new
            if new and outcome.ok:
                outcome.ok = False
                outcome.reason = "footprint"
                outcome.detail = "new files outside the throwaway directory: " + ", ".join(new[:10])
            if dest_dir is not None:
                dest_dir.mkdir(parents=True, exist_ok=True)
                if not probe and out.exists():
                    outcome.png = dest_dir / out.name
                    shutil.copyfile(out, outcome.png)
                if json_path.exists():
                    outcome.json_path = dest_dir / json_path.name
                    shutil.copyfile(json_path, outcome.json_path)
            return outcome
        finally:
            self._cleanup(work)

    def _evaluate(self, entry: Entry, probe: bool, code: Optional[int], stderr: str,
                  out: Path, json_path: Path) -> RunOutcome:
        record: Optional[dict[str, Any]] = None
        if json_path.exists():
            try:
                record = json.loads(json_path.read_bytes().decode("utf-8"))
            except (ValueError, UnicodeDecodeError) as exc:
                return RunOutcome(False, code, "invalid-json", str(exc))
        if code is None:
            return RunOutcome(False, None, "timeout", stderr[-400:])
        if code != 0:
            reason = EXIT_REASONS.get(code, f"exit-{code}")
            detail = ""
            if isinstance(record, dict):
                err = record.get("error") or {}
                if isinstance(err, dict) and err.get("reason"):
                    detail = str(err.get("reason"))
                    if err.get("detail"):
                        detail += f" ({err['detail']})"
                env_part = record if probe else record.get("env")
                if isinstance(env_part, dict) and env_part.get("gate_failures"):
                    detail += " gates: " + ",".join(map(str, env_part["gate_failures"]))
            return RunOutcome(False, code, reason, (detail or stderr[-400:]).strip())
        if record is None:
            return RunOutcome(False, code, "no-json", f"{json_path.name} was not written")
        env_record = record if probe else record.get("env")
        if not isinstance(env_record, dict):
            return RunOutcome(False, code, "no-env", "the record carries no env")
        try:
            env = self.env_info(env_record)
        except PipelineError as exc:
            return RunOutcome(False, code, "env-invalid", str(exc))
        if env_record.get("gate_failures"):
            return RunOutcome(False, code, "environment-gate", ",".join(map(str, env_record["gate_failures"])), env)
        if probe:
            return RunOutcome(True, code, env=env, geometry=None)
        problem = check_geometry(record, out)
        if problem:
            return RunOutcome(False, code, "geometry", problem, env)
        return RunOutcome(True, code, env=env, geometry=record)

    def env_info(self, record: dict[str, Any]) -> EnvInfo:
        if record.get("schema") != envhash.ENV_SCHEMA:
            raise PipelineError(f"unsupported env schema {record.get('schema')!r}")
        core = envhash.env_hash_core(record)
        if record.get("env_hash_core") != core:
            raise PipelineError(
                f"env_hash_core cross-check failed: binary says {record.get('env_hash_core')}, "
                f"recomputed {core}")
        files = fonts.font_files(envhash.font_file_list(record), self.cfg.font_resolver, self._font_cache)
        platform = envhash.platform_tag(record, under_xvfb=bool(self.xvfb))
        return EnvInfo(record, core, envhash.final_env_hash(core, platform, files), platform, files)

    def probe(self, entry: Entry) -> RunOutcome:
        key = entry.probe_key()
        if key not in self._probe_cache:
            self._probe_cache[key] = self._run(entry, probe=True, dest_dir=None, stem="env")
        return self._probe_cache[key]

    def render(self, entry: Entry, dest_dir: Path) -> RunOutcome:
        return self._run(entry, probe=False, dest_dir=dest_dir, stem=entry.id)


def check_geometry(geometry: dict[str, Any], png: Path) -> str:
    if geometry.get("schema") != 1:
        return f"unsupported geometry schema {geometry.get('schema')!r}"
    if geometry.get("error"):
        return f"record carries an error: {geometry['error']}"
    if geometry.get("capture_mode") not in CAPTURE_MODES:
        return f"unknown capture_mode {geometry.get('capture_mode')!r}"
    if geometry.get("dpr") != 2:
        return f"dpr-mismatch: expected 2, got {geometry.get('dpr')!r}"
    if not png.exists():
        return f"{png.name} was not written"
    with Image.open(png) as img:
        actual = list(img.size)
    if list(geometry.get("image_size") or []) != actual:
        return f"image_size {geometry.get('image_size')} does not match the PNG {actual}"
    if not isinstance(geometry.get("widgets"), dict) or not isinstance(geometry.get("missing", []), list):
        return "widgets/missing malformed"
    return ""


def comparable_json(path: Path) -> bytes:
    """A render JSON without the fields that legitimately differ per run."""
    data = load_json(path)
    env = data.get("env") if isinstance(data, dict) else None
    if isinstance(env, dict):
        data["env"] = envhash.strip_volatile(env)
    return canonical_json(data)


def freshness_warnings(binary: Path, gpgfrontend: Path, source_paths: list[str]) -> list[str]:
    """A heuristic, not proof that the binary matches the source."""
    warnings: list[str] = []
    binary = Path(binary)
    for candidate in (binary.parent / "BUILD-INFO.json", binary.parent.parent / "BUILD-INFO.json"):
        if candidate.exists():
            info = load_json(candidate, {}) or {}
            head = gitutil.head(gpgfrontend)
            if info.get("commit") and info.get("commit") != head:
                warnings.append(f"{candidate}: commit {info.get('commit')} differs from GpgFrontend HEAD {head}")
            return warnings
    try:
        bin_mtime = binary.stat().st_mtime
    except OSError:
        return warnings
    newest: tuple[float, str] = (0.0, "")
    for rel in source_paths:
        path = Path(gpgfrontend) / rel
        files = [path] if path.is_file() else (p for p in path.rglob("*") if p.is_file()) if path.is_dir() else []
        for f in files:
            m = f.stat().st_mtime
            if m > newest[0]:
                newest = (m, str(f))
    if newest[0] > bin_mtime:
        warnings.append(f"binary {binary} is older than {newest[1]}; it may not contain the latest source")
    return warnings


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Render or probe manifest entries (debug helper).")
    parser.add_argument("--gpgfrontend", required=True, type=Path)
    parser.add_argument("--binary", type=Path, default=os.environ.get("GF_SCREENSHOT_BINARY"))
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--only", required=True, help="comma separated entry ids")
    parser.add_argument("--probe", action="store_true", help="run --screenshot-env instead")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_CACHE / "render")
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--keep-work", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not args.binary:
            raise UsageError("--binary or GF_SCREENSHOT_BINARY is required")
        manifest: Manifest = load_manifest(args.manifest)
        by_id = manifest.by_id()
        renderer = Renderer(RenderConfig(args.binary, args.gpgfrontend, args.work_root, args.keep_work))
        rc = 0
        for entry_id in split_ids(args.only):
            if entry_id not in by_id or not by_id[entry_id].renderable:
                raise UsageError(f"unknown or non-renderable id: {entry_id}")
            entry = by_id[entry_id]
            outcome = renderer.probe(entry) if args.probe else renderer.render(entry, args.out_dir)
            if outcome.ok and outcome.env:
                print(f"{entry_id}: ok platform={outcome.env.platform} env_hash={outcome.env.env_hash}"
                      + (f" png={outcome.png}" if outcome.png else ""))
            else:
                rc = 1
                print(f"{entry_id}: failed:{outcome.failure}")
        return rc
    except UsageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except PipelineError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
