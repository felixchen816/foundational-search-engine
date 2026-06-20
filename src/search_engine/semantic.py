"""Lightweight semantic query expansion."""

from typing import Dict, Iterable, List, Set

from search_engine.search import tokenize


SEMANTIC_SYNONYMS: Dict[str, Set[str]] = {
    "find": {"search", "retrieve"},
    "interface": {"ui", "web"},
    "quality": {"evaluation", "precision"},
    "rank": {"ranking", "score"},
    "ranking": {"rank", "score"},
    "results": {"documents", "matches"},
    "search": {"find", "retrieve"},
    "ui": {"interface", "web"},
    "web": {"interface", "ui"},
}


def expand_query_terms(query: str, synonyms: Dict[str, Set[str]] = SEMANTIC_SYNONYMS) -> List[str]:
    """Return normalized query terms plus known semantic neighbors."""
    expanded = set()
    for term in tokenize(query):
        expanded.add(term)
        expanded.update(synonyms.get(term, set()))
    return sorted(expanded)


def expand_query_text(query: str) -> str:
    """Return semantic-expanded query text for the existing search pipeline."""
    return " ".join(expand_query_terms(query))
