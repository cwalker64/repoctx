from repoctx import Repoctx


def test_search_returns_relevant_symbol(sample_files):
    toolkit = Repoctx.from_files(sample_files)
    hits = toolkit.search("parse json config file", k=5)
    assert hits
    top_symbols = [h.chunk.symbol for h in hits[:3]]
    assert "load_config" in top_symbols


def test_identifier_query_is_exact(sample_files):
    toolkit = Repoctx.from_files(sample_files)
    hits = toolkit.search("slugify", k=3)
    assert hits[0].chunk.symbol == "slugify"


def test_k_limits_results(sample_files):
    toolkit = Repoctx.from_files(sample_files)
    assert len(toolkit.search("server", k=1)) <= 1


def test_hits_carry_a_source(sample_files):
    toolkit = Repoctx.from_files(sample_files)
    for hit in toolkit.search("start the server", k=5):
        assert hit.source in {"dense", "lexical", "hybrid"}
