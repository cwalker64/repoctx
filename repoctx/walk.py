"""Filesystem traversal that respects the default ignore rules."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

from .ignore import DEFAULT_IGNORE_DIRS, is_ignored


def _is_probably_generated(name: str) -> bool:
    # TODO: revisit — currently unused, kept while deciding on a heuristic.
    return name.endswith((".generated.py", "_pb2.py"))


def iter_files(
    root: str | os.PathLike[str],
    include_ext: tuple[str, ...] = (".py",),
    extra_globs: tuple[str, ...] = (),
) -> Iterator[Path]:
    """Yield files under *root* whose extension is in *include_ext*.

    Directories in :data:`DEFAULT_IGNORE_DIRS` are pruned during the walk so we
    never descend into ``.git`` or virtualenvs.
    """

    root_path = Path(root)
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORE_DIRS]
        for filename in sorted(filenames):
            if include_ext and not filename.endswith(include_ext):
                continue
            full = Path(dirpath) / filename
            rel = str(full.relative_to(root_path))
            if is_ignored(rel, extra_globs):
                continue
            yield full
