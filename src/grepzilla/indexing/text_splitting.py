# ------------------------------------------------------------------------------------------------------------------------
# IMPORTS & MODULES
# ------------------------------------------------------------------------------------------------------------------------

from __future__ import annotations

import hashlib
import json

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters.character import Language

# ------------------------------------------------------------------------------------------------------------------------
# INGESTION PIPELINE: Text Splitter
# ------------------------------------------------------------------------------------------------------------------------

# Mapping of file extensions to programming languages for text splitting.
LANGUAGES_MAPPING: dict[str, str] = {
    ".py": "PYTHON",
    ".js": "JS",
    ".jsx": "JS",
    ".ts": "TS",
    ".tsx": "TS",
    ".rs": "RUST",
    ".go": "GO",
    ".java": "JAVA",
    ".c": "C",
    ".h": "C",
    ".cpp": "CPP",
    ".cc": "CPP",
    ".cxx": "CPP",
    ".cs": "CSHARP",
    ".rb": "RUBY",
    ".php": "PHP",
    ".swift": "SWIFT",
    ".kt": "KOTLIN",
    ".scala": "SCALA",
    ".sql": "SQL",
    ".sh": "POWERSHELL",
}

# Configuration dataclass for the text chunker, defining parameters for text splitting.
@dataclass(frozen=True, slots=True)
class ChunkerConfig:
    chunk_size: int = 1200
    chunk_overlap: int = 150
    preserve_separators: bool = True
    strip_whitespaces: bool = True

    def __post_init__(self):
        if self.chunk_size < 1:
            raise ValueError("chunk_size must be greater that zero.")
        if self.chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be a negative integer.")
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size.")

# Dataclass representing a chunk of text, which can be used for further processing or indexing.
@dataclass(frozen=True, slots=True)
class TextChunk:

    chunk_id: str
    text: str
    chunk_index: int
    start: int
    end: int
    metadata: dict[str, Any] = field(default_factory=dict)

# Class responsible for splitting text into chunks based on the provided configuration.
class TextChunker:
    def __init__(self, config: ChunkerConfig | None = None) -> None:
        self.config = config or ChunkerConfig()

    def split_text(self, text: str, source: str | Path) -> list[TextChunk]:
        """
        Splits the input text into chunks based on the configuration.

        Args:
            text (str): The input text to be split.
            source (str | Path): The source of the text (e.g., file path).

        Returns:
            list[TextChunk]: A list of TextChunk instances representing the split text.
        """

        if not isinstance(text, str):
            raise TypeError("Text parameter must be of Type: str.")

        if not text.strip():
            raise ValueError("Text parameter cannot be empty or whitespace.")

        # Determine the programming language based on the file extension
        language: Language = LANGUAGES_MAPPING.get(Path(source).suffix)

        # Create a RecursiveCharacterTextSplitter instance with the specified configuration
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            preserve_separator=self.config.preserve_separators,
            strip_whitespace=self.config.strip_whitespaces,
            language=language
        )

        # Split the text into chunks
        chunks = splitter.split_text(text)

        # Create TextChunk instances for each chunk
        text_chunks: list[TextChunk] = []
        document_hash = self._hash(text)

        for index, chunk in enumerate(chunks):

            if not chunk.strip():
                continue  # Skip empty or whitespace-only chunks

            # Generate a unique identifer for chunk.
            start = index * self.config.chunk_size
            end = start + len(chunk)

            chunk_fingerprint = {
                "source": str(source),
                "document_hash": document_hash,
                "chunk_index": index,
                "start": start,
                "end": end,
                "chunk_size": self.config.chunk_size,
                "chunk_overlap": self.config.chunk_overlap,
            }

            # Utilize the fingerprint to generate a unique chunk_id for the chunk.
            chunk_id = self._hash(
                json.dumps(
                    chunk_fingerprint, 
                    sort_keys=True,
                    ensure_ascii=False
                )
            )

            # Add TextChunk to the finalized list of text_chunks.
            text_chunks.append(TextChunk(
                chunk_id=chunk_id,
                text=chunk,
                chunk_index=index,
                start=start,
                end=end
            ))

        return text_chunks

    @staticmethod
    def _hash(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()
