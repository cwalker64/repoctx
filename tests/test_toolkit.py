from repoctx import Config, Repoctx


def test_from_files_and_search(sample_files):
    toolkit = Repoctx.from_files(sample_files)
    assert toolkit.search("slugify")


def test_save_and_load(tmp_path, sample_files):
    toolkit = Repoctx.from_files(sample_files)
    toolkit.save(tmp_path / "idx")
    reloaded = Repoctx.load(tmp_path / "idx")
    assert len(reloaded.chunks) == len(toolkit.chunks)
    assert reloaded.search("slugify")


def test_custom_config_dimension():
    toolkit = Repoctx.from_files(
        {"m.py": "def f():\n    return 1\n"}, config=Config(embedding_dim=64)
    )
    assert toolkit.embedder.dim == 64


def test_graph_property_exposed(sample_files):
    toolkit = Repoctx.from_files(sample_files)
    assert len(toolkit.graph) > 0
