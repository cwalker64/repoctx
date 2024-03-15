"""Reciprocal Rank Fusion (RRF).

RRF merges several ranked lists into one using only rank positions, so a dense
cosine score and a BM25 score never have to be put on the same scale.
"""

from __future__ import annotations

from typing import Optional, Sequence


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[str]],
    k: int = 60,
    weights: Optional[Sequence[float]] = None,
) -> list[tuple[str, float]]:
    """Fuse ranked id lists into a single ranking.

    Each item receives ``weight / (k + rank)`` from every list it appears in,
    where ``rank`` is 1-based. Higher is better.
    """

    if weights is None:
        weights = [1.0] * len(rankings)
    if len(weights) != len(rankings):
        raise ValueError("weights must match the number of rankings")

    scores: dict[str, float] = {}
    for ranking, weight in zip(rankings, weights):
        for rank, item in enumerate(ranking):
            scores[item] = scores.get(item, 0.0) + weight / (k + rank + 1)
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
