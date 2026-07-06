from repoctx.index.bm25 import BM25Index

DOCS = {
    "d1": "def read_file(path):\n    return open(path).read()",
    "d2": "def write_file(path, data):\n    open(path, 'w').write(data)",
    "d3": "class HttpClient:\n    def get(self, url):\n        return fetch(url)",
}


def _build() -> BM25Index:
    index = BM25Index()
    index.index(list(DOCS.keys()), list(DOCS.values()))
    return index


def test_index_length():
    assert len(_build()) == 3


def test_ranks_relevant_doc_first():
    index = _build()
    results = index.search("read file")
    assert results
    assert results[0][0] == "d1"


def test_identifier_query_matches():
    index = _build()
    results = index.search("HttpClient url")
    assert results[0][0] == "d3"


def test_unknown_terms_return_nothing():
    index = _build()
    assert index.search("zzz nonexistent token") == []
