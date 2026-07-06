from pathlib import Path

from repoctx.indexer import Indexer

FIXTURE = Path(__file__).parent / "fixtures" / "sample_pkg"


def test_index_path_produces_chunks():
    result = Indexer().index_path(FIXTURE)
    assert len(result.chunks) > 0
    assert result.bm25 is not None
    assert result.graph is not None


def test_symbol_chunks_are_mapped():
    result = Indexer().index_path(FIXTURE)
    assert any(key.endswith(".add") for key in result.symbol_chunks)


def test_graph_has_module_nodes():
    result = Indexer().index_path(FIXTURE)
    nodes = result.graph.nodes()
    assert "calc" in nodes
    assert "greet" in nodes
