from repoctx.text_utils import split_identifier, tokenize_code


def test_split_camel_case():
    assert split_identifier("parseHTTPResponse") == ["parse", "http", "response"]


def test_split_snake_case():
    assert split_identifier("max_chunk_lines") == ["max", "chunk", "lines"]


def test_tokenize_includes_subtokens():
    tokens = tokenize_code("def readFile(): pass")
    assert "readfile" in tokens
    assert "read" in tokens
    assert "file" in tokens


def test_tokenize_empty_string():
    assert tokenize_code("") == []
