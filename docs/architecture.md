# Architecture

The current architecture has one implemented data path:

```text
local directory -> .txt files -> Document objects
```

Implemented module:

- `loader.py`: reads local text files and returns stable document records.

Planned modules:

- tokenizer
- index
- search
- ranking
- CLI search interface
- web interface
