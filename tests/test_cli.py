"""CLI smoke tests."""

from pathlib import Path

from search_engine.cli import search_main


def test_search_cli_prints_ranked_result(tmp_path: Path, capsys) -> None:
    (tmp_path / "doc.txt").write_text("Search engines start with text search.", encoding="utf-8")

    exit_code = search_main(["search", "--data", str(tmp_path)])

    assert exit_code == 0
    assert "doc.txt\tscore=2\tSearch engines start with text search." in capsys.readouterr().out


def test_search_cli_prints_no_results(tmp_path: Path, capsys) -> None:
    (tmp_path / "doc.txt").write_text("Only local notes.", encoding="utf-8")

    exit_code = search_main(["vector", "--data", str(tmp_path)])

    assert exit_code == 0
    assert capsys.readouterr().out == "No results\n"
