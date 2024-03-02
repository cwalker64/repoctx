"""A small, dependency-free Okapi BM25 index for lexical retrieval.

BM25 complements the dense embeddings: it is unbeatable at matching a rare
identifier verbatim, where a hashed embedding can wash the signal out.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Sequence

from ..text_utils import tokenize_code


class BM25Index:
    """Classic Okapi BM25 over tokenized documents."""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self._ids: list[str] = []
        self._tf: list[Counter[str]] = []
        self._doc_len: list[int] = []
        self._df: Counter[str] = Counter()
        self._avg_len = 0.0
        self._n = 0

    def __len__(self) -> int:
        return self._n

    def index(self, ids: Sequence[str], texts: Sequence[str]) -> None:
        """Tokenize *texts* and build the term-frequency postings."""
        for doc_id, text in zip(ids, texts):
            tokens = tokenize_code(text)
            self._ids.append(doc_id)
            self._tf.append(Counter(tokens))
            self._doc_len.append(len(tokens))
            for term in set(tokens):
                self._df[term] += 1
        self._n = len(self._ids)
        if self._n:
            self._avg_len = sum(self._doc_len) / self._n
