# ------------------------------------------------------------------------------------------------------------------------
# IMPORTS & MODULES
# ------------------------------------------------------------------------------------------------------------------------

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Callable

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
)

from ..error import UnsupportedFileTypeError, DocumentLoadError

# ------------------------------------------------------------------------------------------------------------------------
# INGESTION PIPELINE: Test Loaders
# ------------------------------------------------------------------------------------------------------------------------

class DocumentLoader:

    __slots__ = ("root", "max_file_size", "include_hidden", "_loaders")

    def __init__(self, root: Path | str, max_file_size: int=10, include_hidden: bool=False):
        self.root = Path(root).expanduser().resolve(strict=True)
        self.max_file_size = max_file_size * 1024 * 1024
        self.include_hidden = include_hidden

        if max_file_size <= 0:
            raise ValueError(f"Max file size must be greater than 0 - Current value {max_file_size}")

        self._loaders: dict[
            str, Callable[[Path], list[Document]]
        ] = {
            ".txt": self._load_text,
            ".md": self._load_text,
            ".markdown": self._load_text,
            ".rst": self._load_text,
            ".py": self._load_text,
            ".rs": self._load_text,
            ".js": self._load_text,
            ".ts": self._load_text,
            ".yaml": self._load_text,
            ".yml": self._load_text,
            ".toml": self._load_text,
            ".log": self._load_text,
            ".pdf": self._load_pdf,
            ".csv": self._load_csv,
        }

    def load(self, filepath: Path | str) -> list[Document]:
        path = Path(filepath).expanduser()

        if path.is_symlink():
            return []

        try:
            path = path.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise DocumentLoadError(
                f"Cannot resolve file: {filepath}"
            ) from exc

        if not path.is_relative_to(self.root):
            raise DocumentLoadError(f"File is outside configured root: {path}")

        if not path.is_file():
            return []

        relative_path = path.relative_to(self.root)

        if not self.include_hidden and any(
            part.startswith(".") for part in relative_path.parts
        ):
            return []

        if path.stat().st_size > self.max_file_size_bytes:
            raise DocumentLoadError(f"File exceeds size limit: {path}")

        extension = path.suffix.lower()
        loader_factory = self._loaders.get(extension)

        if loader_factory is None:
            raise UnsupportedFileTypeError(f"Unsupported file extension: {extension}")

        # File I/O and parsing may fail transiently; let the indexing
        # worker catch the error and apply its retry policy.
        try:
            documents = loader_factory(path)
            content_hash = self._hash_file(path)
        except Exception as exc:
            if isinstance(exc, DocumentLoadError):
                raise
            raise DocumentLoadError(f"Failed to load {path}: {exc}") from exc

        for document in documents:
            document.metadata.update({
                "source": str(path),
                "relative_path": relative_path.as_posix(),
                "file_name": path.name,
                "file_extension": extension,
                "content_hash": content_hash,
            })

        return documents    

    @staticmethod
    def _load_csv(path: Path) -> list[Document]:
        return CSVLoader(str(path)).load()

    @staticmethod
    def _load_pdf(path: Path) -> list[Document]:
        return PyPDFLoader(str(path)).load()

    @staticmethod
    def _load_text(path: Path) -> list[Document]:
        return TextLoader(str(path), encoding='utf-8', autodetect_encoding=True).load()

    @staticmethod
    def _hash_file(path: Path) -> str:
        digest = sha256()

        # Avoid reading the entire file into memory just to hash it.
        with path.open("rb") as file:
            for block in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(block)

        return digest.hexdigest()