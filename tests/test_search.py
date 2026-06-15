"""Tests for the keyword search prototype."""

from search_engine.loader import Document
from search_engine.index import build_inverted_index
from search_engine.search import SearchResult, search_documents, search_index, tokenize


def test_tokenize_normalizes_terms() -> None:
    assert tokenize("Search, search! Engine-101") == ["search", "search", "engine", "101"]


def test_search_documents_ranks_by_match_count_then_doc_id() -> None:
    documents = [
        Document(doc_id="b.txt", text="search search engines"),
        Document(doc_id="a.txt", text="search basics"),
        Document(doc_id="c.txt", text="unrelated notes"),
    ]

    assert search_documents(documents, "search") == [
        SearchResult(doc_id="b.txt", score=2, preview="search search engines"),
        SearchResult(doc_id="a.txt", score=1, preview="search basics"),
    ]


def test_search_documents_handles_blank_query() -> None:
    documents = [Document(doc_id="a.txt", text="search basics")]

    assert search_documents(documents, "   ") == []


def test_search_index_reuses_prebuilt_index() -> None:
    documents = [
        Document(doc_id="a.txt", text="search basics"),
        Document(doc_id="b.txt", text="ranking only"),
    ]
    index = build_inverted_index(documents, tokenize)

    assert search_index(index, "ranking") == [
        SearchResult(doc_id="b.txt", score=1, preview="ranking only")
    ]
