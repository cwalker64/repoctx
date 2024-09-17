from repoctx.index.store import load_snapshot, save_snapshot
from repoctx.indexer import Indexer


def test_snapshot_roundtrip(tmp_path):
    result = Indexer().index_files({"m.py": "def f():\n    return 1\n"})
    save_snapshot(
        tmp_path / "s",
        chunks=result.chunks,
        vector_index=result.vector_index,
        graph=result.graph,
        embedder_name="hashing",
        config={"embedding_dim": 256},
    )
    data = load_snapshot(tmp_path / "s")
    assert len(data["chunks"]) == len(result.chunks)
    assert data["vector_index"].ids == result.vector_index.ids
    assert "m" in data["graph"].nodes()
    assert data["manifest"]["embedder"] == "hashing"


def test_loaded_chunks_are_equal(tmp_path):
    result = Indexer().index_files({"m.py": "def hello():\n    return 'hi'\n"})
    save_snapshot(
        tmp_path / "s",
        chunks=result.chunks,
        vector_index=result.vector_index,
        graph=result.graph,
        embedder_name="hashing",
    )
    data = load_snapshot(tmp_path / "s")
    assert data["chunks"][0].text == result.chunks[0].text
