"""Document loading utilities."""

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Document:
    """A text document loaded from disk."""

    doc_id: str
    text: str


def load_documents(directory: str) -> List[Document]:
    """Load `.txt` documents from a local directory.

    Document IDs are stable relative paths, which makes later index output
    easier to read and test.
    """
    root = Path(directory)
    if not root.exists():
        raise FileNotFoundError("Document directory does not exist: {}".format(root))
    if not root.is_dir():
        raise NotADirectoryError("Document path is not a directory: {}".format(root))

    documents: List[Document] = []
    for path in sorted(root.rglob("*.txt")):
        if path.is_file():
            doc_id = path.relative_to(root).as_posix()
            documents.append(Document(doc_id=doc_id, text=path.read_text(encoding="utf-8")))

    return documents
