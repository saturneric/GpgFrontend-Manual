"""Read-only git queries against the GpgFrontend repository.

The pipeline never runs git in the Manual repository.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from common import PipelineError


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", "-c", "core.quotepath=off", "-C", str(repo), *args],
            capture_output=True, check=False, timeout=120,
        )
    except OSError as exc:
        raise PipelineError(f"cannot run git: {exc}") from exc


def _out(proc: subprocess.CompletedProcess) -> str:
    return proc.stdout.decode("utf-8", "replace")


def head(repo: Path) -> str:
    proc = _git(repo, "rev-parse", "HEAD")
    if proc.returncode != 0:
        raise PipelineError(f"{repo}: not a git repository with a HEAD commit")
    return _out(proc).strip()


def commit_exists(repo: Path, commit: str) -> bool:
    if not commit:
        return False
    return _git(repo, "cat-file", "-e", f"{commit}^{{commit}}").returncode == 0


def is_ancestor(repo: Path, commit: str, ref: str = "HEAD") -> bool:
    proc = _git(repo, "merge-base", "--is-ancestor", commit, ref)
    if proc.returncode not in (0, 1):
        raise PipelineError(f"git merge-base failed: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.returncode == 0


def changed_since(repo: Path, commit: str, paths: list[str]) -> list[str]:
    if not paths:
        return []
    proc = _git(repo, "diff", "--name-only", commit, "HEAD", "--", *paths)
    if proc.returncode != 0:
        raise PipelineError(f"git diff failed: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return [line for line in _out(proc).splitlines() if line.strip()]


def dirty(repo: Path, paths: list[str]) -> list[str]:
    if not paths:
        return []
    proc = _git(repo, "status", "--porcelain", "--", *paths)
    if proc.returncode != 0:
        raise PipelineError(f"git status failed: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return [line for line in _out(proc).splitlines() if line.strip()]
