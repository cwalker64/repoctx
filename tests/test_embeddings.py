import numpy as np
from repoctx.embeddings.hashing import HashingEmbedder


def test_embeddings_are_deterministic():
    embedder = HashingEmbedder(dim=64)
    first = embedder.embed(["def foo():\n    return 1"])
    second = embedder.embed(["def foo():\n    return 1"])
    assert np.array_equal(first, second)


def test_shape_and_unit_norm():
    embedder = HashingEmbedder(dim=128)
    vectors = embedder.embed(["class Widget:\n    def render(self): ...", "import os"])
    assert vectors.shape == (2, 128)
    norms = np.linalg.norm(vectors, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-5)


def test_related_text_scores_higher():
    embedder = HashingEmbedder(dim=512)
    query = embedder.embed_one("read file from disk")
    close = embedder.embed_one("read file contents from disk")
    far = embedder.embed_one("compute matrix eigenvalues")
    assert float(query @ close) > float(query @ far)


def test_seed_changes_the_projection():
    a = HashingEmbedder(dim=64, seed=1).embed_one("hello world foo bar")
    b = HashingEmbedder(dim=64, seed=2).embed_one("hello world foo bar")
    assert not np.array_equal(a, b)
