from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_readme_describes_only_current_scope() -> None:
    readme = read_text("README.md")

    assert "Bare-bones Python package scaffold" in readme
    assert "Local `.txt` document loader" in readme
    assert "Inverted index for exact keyword lookup" in readme
    assert "Minimal keyword search" in readme
    assert "Transparent ranking" in readme
    assert "not completed features" in readme.replace("\n", " ")
    assert "Status" in readme


def test_changelog_has_no_old_progress_ledger() -> None:
    changelog = read_text("CHANGELOG.md")

    assert "This project history has been reset" in changelog
    assert "minimal keyword search prototype" in changelog
    assert "Not Yet Implemented" in changelog


def test_architecture_lists_current_runtime_path() -> None:
    architecture = read_text("docs/architecture.md")

    assert "loader.py" in architecture
    assert "index.py" in architecture
    assert "ranking.py" in architecture
    assert "search.py" in architecture
    assert "Planned modules" in architecture
    assert "web interface" in architecture


def test_contributing_keeps_scope_honest() -> None:
    contributing = read_text("CONTRIBUTING.md")

    assert "The change does not describe planned features as completed." in contributing
