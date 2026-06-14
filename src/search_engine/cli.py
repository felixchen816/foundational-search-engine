"""Minimal command-line entrypoints for loading and searching local documents."""

import argparse
from typing import Optional, Sequence

from search_engine.loader import load_documents
from search_engine.search import search_documents


def build_load_parser() -> argparse.ArgumentParser:
    """Create the loader parser."""
    parser = argparse.ArgumentParser(description="Load local .txt documents.")
    parser.add_argument(
        "--data",
        default="data/sample_docs",
        help="Directory containing .txt documents.",
    )
    return parser


def build_search_parser() -> argparse.ArgumentParser:
    """Create the search parser."""
    parser = argparse.ArgumentParser(description="Search local .txt documents.")
    parser.add_argument("query", help="Keyword query to search for.")
    parser.add_argument(
        "--data",
        default="data/sample_docs",
        help="Directory containing .txt documents.",
    )
    return parser


def load_main(argv: Optional[Sequence[str]] = None) -> int:
    """Load documents and print their stable IDs."""
    args = build_load_parser().parse_args(argv)
    documents = load_documents(args.data)
    for document in documents:
        print(document.doc_id)
    print("documents={}".format(len(documents)))
    return 0


def search_main(argv: Optional[Sequence[str]] = None) -> int:
    """Search documents and print ranked matches."""
    args = build_search_parser().parse_args(argv)
    documents = load_documents(args.data)
    results = search_documents(documents, args.query)

    if not results:
        print("No results")
        return 0

    for result in results:
        print("{}\tscore={}\t{}".format(result.doc_id, result.score, result.preview))
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Default module entrypoint."""
    return load_main(argv)
