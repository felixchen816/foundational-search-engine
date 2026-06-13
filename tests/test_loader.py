from pathlib import Path

import pytest

from search_engine.loader import Document, load_documents


def test_load_documents_reads_txt_files_with_stable_ids(tmp_path: Path) -> None:
    (tmp_path / "b.txt").write_text("second", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "a.txt").write_text("first", encoding="utf-8")
    (tmp_path / "skip.md").write_text("skip", encoding="utf-8")

    documents = load_documents(str(tmp_path))

    assert documents == [
        Document(doc_id="b.txt", text="second"),
        Document(doc_id="nested/a.txt", text="first"),
    ]


def test_load_documents_rejects_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Document directory does not exist"):
        load_documents(str(tmp_path / "missing"))


def test_load_documents_rejects_file_path(tmp_path: Path) -> None:
    file_path = tmp_path / "doc.txt"
    file_path.write_text("text", encoding="utf-8")

    with pytest.raises(NotADirectoryError, match="Document path is not a directory"):
        load_documents(str(file_path))
