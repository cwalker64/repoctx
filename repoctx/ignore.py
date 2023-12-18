"""Default ignore rules for repository traversal."""

from __future__ import annotations

import fnmatch
from pathlib import PurePath

DEFAULT_IGNORE_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        ".venv",
        "venv",
        "env",
        "node_modules",
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
        "build",
        "dist",
        ".repoctx",
        ".tox",
        ".eggs",
    }
)

DEFAULT_IGNORE_GLOBS: tuple[str, ...] = (
    "*.pyc",
    "*.pyo",
    "*.so",
    "*.min.js",
    "*.lock",
    "*.egg-info",
)


def is_ignored(rel_path: str, extra_globs: tuple[str, ...] = ()) -> bool:
    """Return ``True`` if a repo-relative path should be skipped."""

    parts = PurePath(rel_path).parts
    if any(part in DEFAULT_IGNORE_DIRS for part in parts):
        return True
    name = parts[-1] if parts else rel_path
    for pattern in DEFAULT_IGNORE_GLOBS + tuple(extra_globs):
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel_path, pattern):
            return True
    return False
