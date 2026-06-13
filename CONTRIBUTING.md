# Contributing

Keep changes small, easy to test, and aligned with the current scope.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Workflow

1. Pick one small improvement.
2. Add or update light tests.
3. Update documentation if the public surface changes.
4. Run `python -m pytest`.
5. Commit with a clear descriptive message.

## Pull Request Checklist

- Tests pass locally.
- Documentation matches implemented behavior.
- The change does not describe planned features as completed.
