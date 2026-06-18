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
5. Transparent ranking
6. Example datasets
7. Evaluation

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
terms, builds or reuses the inverted index, applies transparent ranking, and
sorts matches by score descending with document ID as a stable tie-breaker.

## Ranking Contract

Ranking combines term frequency, matched query-term coverage, and a simple
inverse document frequency weight. The score is transparent and deterministic,
so later evaluation can explain why one result outranks another.

## Example Data Contract

The tracked example corpus is intentionally small and topic-focused. It gives
manual CLI testing enough variety to exercise indexing, ranking, and previews
without pretending to be a benchmark. Example queries are plain text so they can
be copied directly into the CLI.

## Evaluation Contract

Evaluation uses small JSONL relevance judgments. Each line names a query and the
document IDs considered relevant. The current metrics are precision@k and mean
reciprocal rank, which are enough to catch obvious ranking regressions before a
larger benchmark exists.

## Planned Stages

- Web interface
