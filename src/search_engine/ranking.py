"""Transparent ranking for indexed keyword search."""

import math
from dataclasses import dataclass
from typing import Iterable, Mapping

from search_engine.index import InvertedIndex


@dataclass(frozen=True)
class RankBreakdown:
    """Explainable score components for a matched document."""

    score: float
    term_frequency: int
    matched_terms: int


def rank_documents(index: InvertedIndex, query_terms: Iterable[str]) -> Mapping[str, RankBreakdown]:
    """Score documents with term frequency, coverage, and rare-term weighting."""
    terms = list(query_terms)
    if not terms:
        return {}

    document_count = max(len(index.documents), 1)
    term_scores = {}
    matched_terms_by_doc = {}
    term_frequency_by_doc = {}

    for term in terms:
        postings = index.postings.get(term, {})
        if not postings:
            continue

        inverse_document_frequency = math.log((document_count + 1) / (len(postings) + 1)) + 1
        for doc_id, term_count in postings.items():
            term_scores[doc_id] = term_scores.get(doc_id, 0.0) + term_count * inverse_document_frequency
            term_frequency_by_doc[doc_id] = term_frequency_by_doc.get(doc_id, 0) + term_count
            matched_terms_by_doc[doc_id] = matched_terms_by_doc.get(doc_id, 0) + 1

    query_term_count = len(set(terms))
    rankings = {}
    for doc_id, base_score in term_scores.items():
        coverage = matched_terms_by_doc[doc_id] / query_term_count
        rankings[doc_id] = RankBreakdown(
            score=base_score * (1 + coverage),
            term_frequency=term_frequency_by_doc[doc_id],
            matched_terms=matched_terms_by_doc[doc_id],
        )

    return rankings
