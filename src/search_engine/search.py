"""Minimal keyword search prototype."""

import re
from dataclasses import dataclass
from typing import Iterable, List

from search_engine.index import InvertedIndex, build_inverted_index
from search_engine.loader import Document


_TERM_PATTERN = re.compile(r"[A-Za-z0-9]+")


@dataclass(frozen=True)
class SearchResult:
    """A document matched by a keyword query."""

    doc_id: str
    score: int
    preview: str


def tokenize(text: str) -> List[str]:
    """Normalize text into lowercase alphanumeric terms."""
    return [match.group(0).lower() for match in _TERM_PATTERN.finditer(text)]


def search_documents(documents: Iterable[Document], query: str) -> List[SearchResult]:
    """Build an inverted index and return ranked keyword matches."""
    index = build_inverted_index(documents, tokenize)
    return search_index(index, query)


def search_index(index: InvertedIndex, query: str) -> List[SearchResult]:
    """Return documents ranked by simple keyword match count."""
    query_terms = tokenize(query)
    if not query_terms:
        return []

    scores = {}
    for term in query_terms:
        for doc_id, count in index.postings.get(term, {}).items():
            scores[doc_id] = scores.get(doc_id, 0) + count

    results = [
        SearchResult(
            doc_id=doc_id,
            score=score,
            preview=index.documents[doc_id].text.strip().replace("\n", " ")[:120],
        )
        for doc_id, score in scores.items()
    ]

    return sorted(results, key=lambda result: (-result.score, result.doc_id))
