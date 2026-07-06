from repoctx.cli import main


def _make_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "m.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    return repo


def test_index_then_search(tmp_path, capsys):
    repo = _make_repo(tmp_path)
    index_dir = tmp_path / "idx"
    assert main(["index", str(repo), "-o", str(index_dir)]) == 0
    assert "indexed" in capsys.readouterr().out

    assert main(["search", "add two numbers", "--index", str(index_dir)]) == 0
    assert "m.py" in capsys.readouterr().out


def test_graph_and_info(tmp_path, capsys):
    repo = _make_repo(tmp_path)
    index_dir = tmp_path / "idx"
    main(["index", str(repo), "-o", str(index_dir)])
    capsys.readouterr()

    assert main(["graph", "--index", str(index_dir)]) == 0
    assert "nodes:" in capsys.readouterr().out

    assert main(["info", "--index", str(index_dir)]) == 0
    assert "embedder" in capsys.readouterr().out


def test_no_command_returns_error():
    assert main([]) == 1
