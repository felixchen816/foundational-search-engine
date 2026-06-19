"""Minimal command-line entrypoints for loading and searching local documents."""

import argparse
from typing import Optional, Sequence

from search_engine.evaluation import evaluate_corpus, mean_precision_at_k, mean_reciprocal_rank
from search_engine.loader import load_documents
from search_engine.search import search_documents
from search_engine.web import DEFAULT_DATA_DIRECTORY, run_server


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


def build_evaluate_parser() -> argparse.ArgumentParser:
    """Create the evaluation parser."""
    parser = argparse.ArgumentParser(description="Evaluate local search results.")
    parser.add_argument(
        "--data",
        default="data/example_corpus",
        help="Directory containing .txt documents.",
    )
    parser.add_argument(
        "--judgments",
        default="data/relevance/example_queries.jsonl",
        help="JSONL file with query relevance judgments.",
    )
    parser.add_argument("--k", type=int, default=3, help="Cutoff for precision@k.")
    return parser


def build_web_parser() -> argparse.ArgumentParser:
    """Create the web server parser."""
    parser = argparse.ArgumentParser(description="Run the local search web UI.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind.")
    parser.add_argument(
        "--data",
        default=DEFAULT_DATA_DIRECTORY,
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
        print("{}\tscore={:.3f}\t{}".format(result.doc_id, result.score, result.preview))
    return 0


def evaluate_main(argv: Optional[Sequence[str]] = None) -> int:
    """Evaluate judged queries and print summary metrics."""
    args = build_evaluate_parser().parse_args(argv)
    results = evaluate_corpus(args.data, args.judgments, k=args.k)
    for result in results:
        print(
            "{}\tprecision@{}={:.3f}\tmrr={:.3f}\tfound={}".format(
                result.query,
                args.k,
                result.precision_at_k,
                result.reciprocal_rank,
                result.relevant_found,
            )
        )
    print("mean_precision@{}={:.3f}".format(args.k, mean_precision_at_k(results)))
    print("mean_reciprocal_rank={:.3f}".format(mean_reciprocal_rank(results)))
    return 0


def web_main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the local web UI."""
    args = build_web_parser().parse_args(argv)
    run_server(args.host, args.port, args.data)
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Default module entrypoint."""
    return load_main(argv)
