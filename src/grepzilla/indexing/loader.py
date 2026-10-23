# ------------------------------------------------------------------------------------------------------------------------
# IMPORTS & MODULES
# ------------------------------------------------------------------------------------------------------------------------

from __future__ import annotations

import csv
import json
import tomllib

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
)

# ------------------------------------------------------------------------------------------------------------------------
# INGESTION PIPELINE: Test Loaders
# ------------------------------------------------------------------------------------------------------------------------

class DocumentLoader:
    pass