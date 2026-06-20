"""CLI smoke tests."""

from pathlib import Path

from search_engine.cli import evaluate_main, search_main


def test_search_cli_prints_ranked_result(tmp_path: Path, capsys) -> None:
    (tmp_path / "doc.txt").write_text("Search engines start with text search.", encoding="utf-8")

    exit_code = search_main(["search", "--data", str(tmp_path)])

    assert exit_code == 0
    assert "doc.txt\tscore=4.000\tSearch engines start with text search." in capsys.readouterr().out


def test_search_cli_prints_no_results(tmp_path: Path, capsys) -> None:
    (tmp_path / "doc.txt").write_text("Only local notes.", encoding="utf-8")

    exit_code = search_main(["vector", "--data", str(tmp_path)])

    assert exit_code == 0
    assert capsys.readouterr().out == "No results\n"


def test_search_cli_supports_semantic_mode(capsys) -> None:
    exit_code = search_main(["find", "--mode", "semantic", "--data", "data/example_corpus"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "search_engine.txt" in output


def test_evaluate_cli_prints_summary_metrics(capsys) -> None:
    exit_code = evaluate_main([])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "search index\tprecision@3=" in output
    assert "mean_precision@3=" in output
    assert "mean_reciprocal_rank=1.000" in output
