# Architecture

The current architecture has one implemented data path:

```text
local directory -> .txt files -> Document objects -> keyword SearchResult objects
```

Implemented modules:

- `loader.py`: reads local text files and returns stable document records.
- `search.py`: tokenizes query and document text, counts exact keyword matches,
  and returns ranked result records.
- `cli.py`: exposes loader and search smoke-test commands.

Planned modules:

- index
- production ranking
- web interface
