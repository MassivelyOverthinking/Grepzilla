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

def validate_yaml_file(path: Path) -> Path:
    if not isinstance(path, Path):
        raise typer.BadParameter("Filepath must be a Path object.")

    if not path.exists():
        raise typer.BadParameter(f"Filepath '{path}' does not exist.")

    if not path.is_file():
        raise typer.BadParameter(f"Filepath '{path}' is not a file.")

    if path.suffix.lower() not in {".yaml", ".yml"}:
        raise typer.BadParameter(f"Filepath '{path}' is not a YAML file.")

    return path