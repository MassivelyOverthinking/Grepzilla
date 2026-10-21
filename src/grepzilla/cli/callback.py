# ------------------------------------------------------------------------------------------------------------------------
# IMPORTS & MODULES
# ------------------------------------------------------------------------------------------------------------------------

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

# ------------------------------------------------------------------------------------------------------------------------
# GREPZILLA CLI: Custom Callbacks
# ------------------------------------------------------------------------------------------------------------------------

def validate_dir(path: str) -> Path:
    if not isinstance(path, str) or not path.strip():
        raise typer.BadParameter("Filepath must be a non-empty string.")

    path = Path(path).expanduser().resolve()

    if not path.exists():
        raise typer.BadParameter(f"Filepath '{path}' does not exist.")

    if not path.is_dir():
        raise typer.BadParameter(f"Filepath '{path}' is not a directory.")

    return path

def validate_config_file(path: str) -> Path:
    if not isinstance(path, str) or not path.strip():
        raise typer.BadParameter("Filepath must be a non-empty string.")

    path = Path(path).expanduser().resolve()

    if not path.exists():
        raise typer.BadParameter(f"Filepath '{path}' does not exist.")

    if not path.is_file():
        raise typer.BadParameter(f"Filepath '{path}' is not a file.")

    if path.suffix.lower() not in {".yaml", ".yml"}:
        raise typer.BadParameter(f"Filepath '{path}' is not a YAML file.")

    return path