"""Tests for transparent ranking."""

from search_engine.index import build_inverted_index
from search_engine.loader import Document
from search_engine.ranking import rank_documents
from search_engine.search import tokenize


def test_rank_documents_rewards_term_frequency_and_coverage() -> None:
    index = build_inverted_index(
        [
            Document(doc_id="a.txt", text="search search ranking"),
            Document(doc_id="b.txt", text="search basics"),
            Document(doc_id="c.txt", text="ranking only"),
        ],
        tokenize,
    )

    rankings = rank_documents(index, ["search", "ranking"])

    assert rankings["a.txt"].score > rankings["b.txt"].score
    assert rankings["a.txt"].score > rankings["c.txt"].score
    assert rankings["a.txt"].term_frequency == 3
    assert rankings["a.txt"].matched_terms == 2


def test_rank_documents_handles_no_matching_terms() -> None:
    index = build_inverted_index([Document(doc_id="a.txt", text="search basics")], tokenize)

    assert rank_documents(index, ["missing"]) == {}
