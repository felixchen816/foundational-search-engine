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
- `cli.py`: exposes loader and search smoke-test commands.

Planned modules:

- web interface
