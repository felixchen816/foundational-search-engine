# Design Notes

## Scope

The project is intentionally back at the foundation. The only implemented
runtime behavior is loading local `.txt` documents from disk.

## Completed Stages

1. Bare-bones project scaffold
2. Local document loader

## Loader Contract

The loader accepts a directory path, recursively finds `.txt` files, reads them
as UTF-8, and returns `Document` objects with stable IDs relative to the loaded
root. Stable IDs make later indexing and tests easier to reason about.

## Planned Stages

- Tokenizer
- Inverted index
- Keyword search
- Ranking
- CLI search interface
- Example datasets
- Evaluation
- Web interface
