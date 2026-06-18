# Architecture

The current architecture has one implemented data path:

```text
local directory -> .txt files -> Document objects -> InvertedIndex -> SearchResult objects
```

Implemented modules:

- `loader.py`: reads local text files and returns stable document records.
- `index.py`: builds term postings with per-document occurrence counts.
- `ranking.py`: assigns transparent scores from term frequency, coverage, and
  rare-term weighting.
- `search.py`: tokenizes queries, runs indexed lookup, applies ranking, and
  returns result records.
- `evaluation.py`: runs judged queries and computes precision@k and reciprocal
  rank.
- `cli.py`: exposes loader and search smoke-test commands.

Tracked data:

- `data/sample_docs`: tiny loader smoke-test corpus.
- `data/example_corpus`: small manual-testing corpus for search topics.
- `data/example_queries.txt`: starter CLI queries for the example corpus.
- `data/relevance/example_queries.jsonl`: relevance judgments for evaluation.

Planned modules:

- web interface
