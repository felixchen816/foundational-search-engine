"""Evaluation helpers for judged keyword-search queries."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Set

from search_engine.loader import load_documents
from search_engine.search import search_documents


@dataclass(frozen=True)
class JudgedQuery:
    """A query with known relevant document IDs."""

    query: str
    relevant_doc_ids: Set[str]


@dataclass(frozen=True)
class EvaluationResult:
    """Metrics for one judged query."""

    query: str
    ranked_doc_ids: List[str]
    precision_at_k: float
    reciprocal_rank: float
    relevant_found: int


def precision_at_k(ranked_doc_ids: Iterable[str], relevant_doc_ids: Set[str], k: int) -> float:
    """Return the fraction of top-k results that are relevant."""
    if k <= 0:
        raise ValueError("k must be positive")

    top_k = list(ranked_doc_ids)[:k]
    if not top_k:
        return 0.0

    return sum(doc_id in relevant_doc_ids for doc_id in top_k) / k


def reciprocal_rank(ranked_doc_ids: Iterable[str], relevant_doc_ids: Set[str]) -> float:
    """Return reciprocal rank of the first relevant result."""
    for index, doc_id in enumerate(ranked_doc_ids, start=1):
        if doc_id in relevant_doc_ids:
            return 1 / index
    return 0.0


def evaluate_ranked_results(
    query: str,
    ranked_doc_ids: Iterable[str],
    relevant_doc_ids: Set[str],
    k: int = 3,
) -> EvaluationResult:
    """Evaluate one ranked list against relevant document IDs."""
    ranked = list(ranked_doc_ids)
    found = sum(doc_id in relevant_doc_ids for doc_id in ranked)
    return EvaluationResult(
        query=query,
        ranked_doc_ids=ranked,
        precision_at_k=precision_at_k(ranked, relevant_doc_ids, k),
        reciprocal_rank=reciprocal_rank(ranked, relevant_doc_ids),
        relevant_found=found,
    )


def load_judged_queries(path: str) -> List[JudgedQuery]:
    """Load JSONL judged queries."""
    judged_queries: List[JudgedQuery] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        judged_queries.append(
            JudgedQuery(
                query=row["query"],
                relevant_doc_ids=set(row["relevant_doc_ids"]),
            )
        )
    return judged_queries


def evaluate_corpus(data_directory: str, judgments_path: str, k: int = 3) -> List[EvaluationResult]:
    """Run judged queries against a local corpus."""
    documents = load_documents(data_directory)
    results: List[EvaluationResult] = []
    for judged_query in load_judged_queries(judgments_path):
        ranked_doc_ids = [result.doc_id for result in search_documents(documents, judged_query.query)]
        results.append(
            evaluate_ranked_results(
                judged_query.query,
                ranked_doc_ids,
                judged_query.relevant_doc_ids,
                k=k,
            )
        )
    return results


def mean_precision_at_k(results: Iterable[EvaluationResult]) -> float:
    """Return mean precision@k over evaluated queries."""
    values = [result.precision_at_k for result in results]
    return sum(values) / len(values) if values else 0.0


def mean_reciprocal_rank(results: Iterable[EvaluationResult]) -> float:
    """Return mean reciprocal rank over evaluated queries."""
    values = [result.reciprocal_rank for result in results]
    return sum(values) / len(values) if values else 0.0
