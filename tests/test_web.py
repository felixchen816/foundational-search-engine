"""Tests for the standard-library web UI."""

from search_engine.web import render_search_page, search_request


def test_render_search_page_shows_form() -> None:
    html = render_search_page()

    assert "Foundational Search Engine" in html
    assert 'placeholder="Search local documents"' in html
    assert 'name="data"' in html


def test_search_request_returns_results_for_example_corpus() -> None:
    html, status = search_request("ranking documents", data_directory="data/example_corpus")

    assert status == 200
    assert "ranking.txt" in html
    assert "score=" in html
    assert "Ranking decides" in html


def test_search_request_reports_no_results() -> None:
    html, status = search_request("zzzzzz", data_directory="data/example_corpus")

    assert status == 200
    assert "No results" in html


def test_search_request_escapes_query_and_result_html(tmp_path) -> None:
    (tmp_path / "doc.txt").write_text("<script>alert(1)</script> search", encoding="utf-8")

    html, status = search_request("<query>", data_directory=str(tmp_path))

    assert status == 200
    assert "&lt;query&gt;" in html
    assert "<script>" not in html


def test_search_request_reports_bad_data_directory() -> None:
    html, status = search_request("search", data_directory="missing")

    assert status == 400
    assert "Document directory does not exist" in html
