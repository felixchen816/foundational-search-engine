# Architecture

The current architecture has one implemented data path:

```text
local directory -> .txt files -> Document objects -> InvertedIndex -> SearchResult objects
```

Implemented modules:

- `loader.py`: reads local text files and returns stable document records.
- `index.py`: builds term postings with per-document occurrence counts.
- `search.py`: tokenizes query and document text, counts exact keyword matches,
  and returns ranked result records.
- `cli.py`: exposes loader and search smoke-test commands.

Planned modules:

- production ranking
- web interface
