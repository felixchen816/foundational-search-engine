# Foundational Search Engine

A small, learning-first search engine project. The current repository has a
bare-bones Python package scaffold, a local text document loader, and a tiny
keyword search prototype you can run from the command line.

[![CI](https://github.com/felixchen816/foundational-search-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/felixchen816/foundational-search-engine/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Status

Implemented:

- Bare-bones Python package scaffold
- Local `.txt` document loader
- Inverted index for exact keyword lookup
- Minimal keyword search over loaded documents
- Transparent ranking with term frequency, query coverage, and rare-term weight
- Example corpus and starter queries for manual testing
- Light tests for loader, search, CLI behavior, and repository documentation

Planned:

- Evaluation
- Web UI

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest
```

Load local text files:

```bash
foundational-load --data data/sample_docs
```

Search local text files:

```bash
foundational-search search --data data/sample_docs
```

Try the richer example corpus:

```bash
foundational-search "ranking documents" --data data/example_corpus
```

Use the loader from Python:

```python
from search_engine.loader import load_documents
from search_engine.index import build_inverted_index
from search_engine.search import search_documents
from search_engine.search import search_index, tokenize

documents = load_documents("data/sample_docs")
index = build_inverted_index(documents, tokenize)
results = search_index(index, "search")
for result in results:
    print(result.doc_id, result.score, result.preview)
```

## Framework

```text
foundational-search-engine/
  data/sample_docs/      Tiny local text corpus for loader checks
  data/example_corpus/   Small topic corpus for manual search testing
  data/example_queries.txt
  docs/                  Short design notes
  src/search_engine/     Python package
  tests/                 Light pytest coverage
```

## Current API

`load_documents(directory: str) -> list[Document]`

- Recursively reads `.txt` files.
- Returns stable document IDs relative to the input directory.
- Reads file text as UTF-8.
- Raises clear filesystem errors for missing paths or non-directory paths.

`search_documents(documents: Iterable[Document], query: str) -> list[SearchResult]`

- Builds an inverted index for the provided documents.
- Tokenizes text into lowercase alphanumeric terms.
- Scores documents with term frequency, query coverage, and rare-term weight.
- Sorts results by score descending, then document ID.
- Returns a short preview from each matched document.

`build_inverted_index(documents: Iterable[Document], terms_by_text) -> InvertedIndex`

- Stores each term with per-document occurrence counts.
- Keeps loaded documents available for result previews.
- Supports direct `search_index(index, query)` calls when callers want to reuse
  a prebuilt index.

## Development

```bash
python -m pytest
```

The project intentionally has no semantic search, evaluation framework, or web
server yet. Those pieces are roadmap items, not completed features.

## License

MIT. See [LICENSE](LICENSE).
