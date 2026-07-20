import subprocess
import time
from pathlib import Path
from shutil import which

from platformdirs import user_cache_path

from ignorante import IGNORANTE

REPOSITORY_URL = "https://github.com/github/gitignore.git"
UPDATE_INTERVAL = 60 * 60 * 24  # 1 day, in seconds


def get_repository() -> Path:
    """Return the root of a local, always up-to-date clone of github/gitignore.

    The clone lives in the user's cache directory. It is created on first use
    and pulled at most once a day on subsequent calls.
    """
    if which("git") is None:
        raise RuntimeError("git is required by ignorante but was not found on PATH.")

    repo_path = user_cache_path(IGNORANTE, ensure_exists=True) / "gitignore"

    if not (repo_path / ".git").exists():
        _run_git("clone", "--depth", "1", REPOSITORY_URL, str(repo_path))
    elif _seconds_since_last_pull(repo_path) >= UPDATE_INTERVAL:
        _run_git("pull", "--depth", "1", cwd=repo_path)

    return repo_path


def _seconds_since_last_pull(repo_path: Path) -> float:
    # git touches .git/FETCH_HEAD on every fetch/pull, so its mtime doubles as a
    # "last updated" timestamp without needing to persist one ourselves.
    fetch_head = repo_path / ".git" / "FETCH_HEAD"

    if not fetch_head.exists():
        return float("inf")

    return time.time() - fetch_head.stat().st_mtime


def _run_git(*args: str, cwd: Path | None = None) -> None:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"git {args[0]} failed: {result.stderr.strip()}")
