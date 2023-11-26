"""Lightweight code tokenization used by the lexical index and hashing embedder.

We deliberately avoid heavyweight NLP here: identifiers are split into their
sub-tokens (``snake_case`` and ``camelCase`` are both broken apart) so that a
query for ``read file`` still matches a ``readFile`` definition.
"""

from __future__ import annotations

import re

_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_SUBTOKEN_RE = re.compile(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|[0-9]+")


def split_identifier(identifier: str) -> list[str]:
    """Break an identifier into lowercase sub-tokens.

    ``"parseHTTPResponse"`` -> ``["parse", "http", "response"]`` and
    ``"max_chunk_lines"`` -> ``["max", "chunk", "lines"]``.
    """

    parts: list[str] = []
    for piece in identifier.split("_"):
        if not piece:
            continue
        parts.extend(m.group(0).lower() for m in _SUBTOKEN_RE.finditer(piece))
    return parts


def tokenize_code(text: str) -> list[str]:
    """Tokenize source text into a bag of identifiers and their sub-tokens."""

    tokens: list[str] = []
    for match in _IDENT_RE.finditer(text):
        identifier = match.group(0)
        tokens.append(identifier.lower())
        subs = split_identifier(identifier)
        if len(subs) > 1:
            tokens.extend(subs)
    return tokens
