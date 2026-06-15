"""Small inverted index for local text documents."""

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping

from search_engine.loader import Document


@dataclass(frozen=True)
class InvertedIndex:
    """Term lookup table with the source documents kept for result previews."""

    postings: Mapping[str, Mapping[str, int]]
    documents: Mapping[str, Document]


def build_inverted_index(documents: Iterable[Document], terms_by_text) -> InvertedIndex:
    """Build term -> document -> count postings for loaded documents."""
    postings: Dict[str, Dict[str, int]] = {}
    documents_by_id: Dict[str, Document] = {}

    for document in documents:
        documents_by_id[document.doc_id] = document
        for term in terms_by_text(document.text):
            term_postings = postings.setdefault(term, {})
            term_postings[document.doc_id] = term_postings.get(document.doc_id, 0) + 1

    return InvertedIndex(postings=postings, documents=documents_by_id)
