#========================================================================================================================
# IMPORTS & MODULES
#========================================================================================================================

from __future__ import annotations

import hashlib
import json

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters.character import Language

#========================================================================================================================
# INGESTION PIPELINE: Text Splitter
#========================================================================================================================

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
    pass

# Dataclass representing a chunk of text, which can be used for further processing or indexing.
@dataclass(frozen=True, slots=True)
class TextChunk:
    pass

# Class responsible for splitting text into chunks based on the provided configuration.
class TextChunker:
    pass
