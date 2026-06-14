"""Minimal keyword search prototype."""

import re
from dataclasses import dataclass
from typing import Iterable, List

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
    """Return documents ranked by simple keyword match count."""
    query_terms = tokenize(query)
    if not query_terms:
        return []

    results: List[SearchResult] = []
    for document in documents:
        document_terms = tokenize(document.text)
        score = sum(document_terms.count(term) for term in query_terms)
        if score > 0:
            results.append(
                SearchResult(
                    doc_id=document.doc_id,
                    score=score,
                    preview=document.text.strip().replace("\n", " ")[:120],
                )
            )

    return sorted(results, key=lambda result: (-result.score, result.doc_id))
