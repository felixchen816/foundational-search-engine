# Foundational Search Engine

A small, learning-first search engine project. The current repository is reset to
the first two milestones: a bare-bones Python package scaffold and a local text
document loader.

[![CI](https://github.com/felixchen816/foundational-search-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/felixchen816/foundational-search-engine/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Status

Implemented:

- Bare-bones Python package scaffold
- Local `.txt` document loader
- Light tests for loader behavior and repository documentation

Planned:

- Tokenization
- Inverted index
- Keyword search API
- Command-line search
- Ranking
- Example corpora and evaluation
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

Use the loader from Python:

```python
from search_engine.loader import load_documents

documents = load_documents("data/sample_docs")
for document in documents:
    print(document.doc_id, len(document.text))
```

## Framework

```text
foundational-search-engine/
  data/sample_docs/      Tiny local text corpus for loader checks
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

## Development

```bash
python -m pytest
```

The project intentionally has no search index, ranking, semantic search,
evaluation framework, or web server yet. Those pieces are roadmap items, not
completed features.

## License

MIT. See [LICENSE](LICENSE).
