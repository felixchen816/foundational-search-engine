"""Tests for the tracked example corpus."""

from pathlib import Path

from search_engine.loader import load_documents
from search_engine.search import search_documents


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_CORPUS = PROJECT_ROOT / "data" / "example_corpus"
EXAMPLE_QUERIES = PROJECT_ROOT / "data" / "example_queries.txt"


def test_example_corpus_loads_multiple_documents() -> None:
    documents = load_documents(str(EXAMPLE_CORPUS))

    assert [document.doc_id for document in documents] == [
        "evaluation.txt",
        "interface.txt",
        "ranking.txt",
        "search_engine.txt",
    ]


def test_example_corpus_supports_representative_queries() -> None:
    documents = load_documents(str(EXAMPLE_CORPUS))
    queries = [line.strip() for line in EXAMPLE_QUERIES.read_text(encoding="utf-8").splitlines()]

    assert queries == ["search index", "ranking documents", "result quality", "web interface"]
    for query in queries:
        assert search_documents(documents, query), "expected at least one result for {!r}".format(query)


def test_example_corpus_ranking_query_finds_ranking_document_first() -> None:
    documents = load_documents(str(EXAMPLE_CORPUS))

    results = search_documents(documents, "ranking documents")

    assert results[0].doc_id == "ranking.txt"
