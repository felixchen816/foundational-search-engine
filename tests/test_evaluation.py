"""Tests for judged-query evaluation."""

from pathlib import Path

import pytest

from search_engine.evaluation import (
    evaluate_corpus,
    evaluate_ranked_results,
    load_judged_queries,
    mean_precision_at_k,
    mean_reciprocal_rank,
    precision_at_k,
    reciprocal_rank,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_precision_at_k_and_reciprocal_rank() -> None:
    ranked = ["a.txt", "b.txt", "c.txt"]
    relevant = {"b.txt", "d.txt"}

    assert precision_at_k(ranked, relevant, 2) == 0.5
    assert reciprocal_rank(ranked, relevant) == 0.5


def test_precision_at_k_rejects_invalid_k() -> None:
    with pytest.raises(ValueError, match="k must be positive"):
        precision_at_k(["a.txt"], {"a.txt"}, 0)


def test_evaluate_ranked_results_summarizes_one_query() -> None:
    result = evaluate_ranked_results("search", ["a.txt", "b.txt"], {"b.txt"}, k=2)

    assert result.query == "search"
    assert result.precision_at_k == 0.5
    assert result.reciprocal_rank == 0.5
    assert result.relevant_found == 1


def test_load_judged_queries_reads_jsonl() -> None:
    judged_queries = load_judged_queries(str(PROJECT_ROOT / "data" / "relevance" / "example_queries.jsonl"))

    assert judged_queries[0].query == "search index"
    assert judged_queries[0].relevant_doc_ids == {"search_engine.txt"}


def test_evaluate_corpus_scores_example_queries() -> None:
    results = evaluate_corpus(
        str(PROJECT_ROOT / "data" / "example_corpus"),
        str(PROJECT_ROOT / "data" / "relevance" / "example_queries.jsonl"),
        k=3,
    )

    assert len(results) == 4
    assert mean_precision_at_k(results) > 0
    assert mean_reciprocal_rank(results) == 1.0
