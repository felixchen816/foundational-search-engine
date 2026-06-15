# Design Notes

## Scope

The project is intentionally still close to the foundation. The implemented
runtime behavior is loading local `.txt` documents from disk and running a
minimal indexed keyword search over them.

## Completed Stages

1. Bare-bones project scaffold
2. Local document loader
3. Minimal keyword search prototype
4. Inverted index

## Loader Contract

The loader accepts a directory path, recursively finds `.txt` files, reads them
as UTF-8, and returns `Document` objects with stable IDs relative to the loaded
root. Stable IDs make later indexing and tests easier to reason about.

## Index Contract

The index stores each normalized term with document IDs and occurrence counts.
It keeps the original loaded documents so search results can include previews
without rereading files.

## Search Contract

The prototype tokenizes query and document text into lowercase alphanumeric
terms, builds or reuses the inverted index, scores each document by exact
keyword match count, and sorts matches by score descending with document ID as a
stable tie-breaker.

## Planned Stages

- Production ranking
- Example datasets
- Evaluation
- Web interface
