"""Tests for lightweight semantic query expansion."""

from search_engine.semantic import expand_query_terms, expand_query_text


def test_expand_query_terms_adds_known_neighbors() -> None:
    assert expand_query_terms("find ui") == ["find", "interface", "retrieve", "search", "ui", "web"]


def test_expand_query_terms_preserves_unknown_terms() -> None:
    assert expand_query_terms("custom topic") == ["custom", "topic"]


def test_expand_query_text_returns_searchable_text() -> None:
    assert expand_query_text("web") == "interface ui web"
