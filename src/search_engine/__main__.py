"""Allow `python -m search_engine` to run the loader CLI."""

from search_engine.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
