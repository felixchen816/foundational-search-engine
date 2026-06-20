# Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run tests:

```bash
python -m pytest
```

Load the sample documents:

```bash
foundational-load --data data/sample_docs
```

Search local documents:

```bash
foundational-search search --data data/sample_docs
```

Search the example corpus:

```bash
foundational-search "ranking documents" --data data/example_corpus
```

Evaluate the example corpus:

```bash
foundational-evaluate
```

Run the local web UI:

```bash
foundational-web --data data/example_corpus --port 8000
```

Try semantic expansion:

```bash
foundational-search find --mode semantic --data data/example_corpus
```
