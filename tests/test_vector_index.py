import numpy as np
import pytest

from repoctx.index.vector_index import VectorIndex


def _build() -> VectorIndex:
    index = VectorIndex(3)
    index.add(
        ["a", "b", "c"],
        np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32),
    )
    return index


def test_add_and_len():
    index = _build()
    assert len(index) == 3
    assert index.ids == ["a", "b", "c"]


def test_search_ranks_nearest_first():
    index = _build()
    results = index.search(np.array([0.9, 0.1, 0.0]), k=2)
    assert results[0][0] == "a"
    assert len(results) == 2
    assert results[0][1] > results[1][1]


def test_search_on_empty_index():
    assert VectorIndex(4).search(np.ones(4)) == []


def test_save_and_load_roundtrip(tmp_path):
    index = _build()
    index.save(tmp_path / "vi")
    loaded = VectorIndex.load(tmp_path / "vi")
    assert loaded.ids == index.ids
    assert loaded.search(np.array([0, 0, 1.0]))[0][0] == "c"


def test_dimension_mismatch_raises():
    index = VectorIndex(3)
    with pytest.raises(ValueError):
        index.add(["x"], np.zeros((1, 4), dtype=np.float32))
