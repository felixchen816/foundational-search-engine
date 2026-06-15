"""Tests for the inverted index."""

from search_engine.index import build_inverted_index
from search_engine.loader import Document
from search_engine.search import tokenize


def test_build_inverted_index_counts_terms_by_document() -> None:
    index = build_inverted_index(
        [
            Document(doc_id="a.txt", text="search search basics"),
            Document(doc_id="b.txt", text="ranking search"),
        ],
        tokenize,
    )

    assert index.postings["search"] == {"a.txt": 2, "b.txt": 1}
    assert index.postings["ranking"] == {"b.txt": 1}
    assert index.documents["a.txt"].text == "search search basics"


def test_build_inverted_index_handles_empty_input() -> None:
    index = build_inverted_index([], tokenize)

    assert index.postings == {}
    assert index.documents == {}
