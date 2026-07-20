from pathlib import Path

from ignorante.repository import get_repository


def find_templates() -> dict[str, Path]:
    """Map every template name, in original casing, to its file.

    e.g. "Python" -> repo/Python.gitignore, "Global/Linux" -> repo/Global/Linux.gitignore,
    "community/Golang/Hugo" -> repo/community/Golang/Hugo.gitignore.
    """
    repo = get_repository()
    return {path.relative_to(repo).with_suffix("").as_posix(): path for path in repo.rglob("*.gitignore")}


def sort_key(name: str) -> tuple[int, str]:
    """Sort key that groups root-level templates first, then Global/, then community/.

    Each group is sorted lexicographically, case-insensitively, within itself.
    """
    group = {"global": 1, "community": 2}.get(name.split("/", 1)[0].lower(), 0)
    return group, name.lower()
