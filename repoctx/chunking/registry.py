"""Map file extensions to chunkers.

Filled in as concrete chunkers land; for now this is a thin placeholder.
"""

from __future__ import annotations


def supported_extensions() -> tuple[str, ...]:
    """Extensions we have a dedicated chunker for."""
    return (".py",)
