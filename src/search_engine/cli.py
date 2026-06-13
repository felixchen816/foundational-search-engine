"""Minimal command-line entrypoint for loading local documents."""

import argparse
from typing import Optional, Sequence

from search_engine.loader import load_documents


def build_parser() -> argparse.ArgumentParser:
    """Create the loader parser."""
    parser = argparse.ArgumentParser(description="Load local .txt documents.")
    parser.add_argument(
        "--data",
        default="data/sample_docs",
        help="Directory containing .txt documents.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Load documents and print their stable IDs."""
    args = build_parser().parse_args(argv)
    documents = load_documents(args.data)
    for document in documents:
        print(document.doc_id)
    print("documents={}".format(len(documents)))
    return 0
