# ------------------------------------------------------------------------------------------------------------------------
# IMPORTS & MODULES
# ------------------------------------------------------------------------------------------------------------------------

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .callback import validate_yaml_file

# ------------------------------------------------------------------------------------------------------------------------
# GREPZILLA CLI: Application Entry Point
# ------------------------------------------------------------------------------------------------------------------------

app = typer.Typer(
    name="Grepzilla",
    help="Grepzilla: Semantic file search tool.",
    no_args_is_help=True,
)

@app.command(
    name="setup",
    help="Setup Grepzilla configuration and orchestration using YAML config-file.",
)
def setup(
    path: Annotated[
        Path, 
        typer.Argument(
            help="Path to the YAML configuration file.", 
            prompt="Please enter filepath to YAML config-file.",
            callback=validate_yaml_file,
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        )
    ],
):
    """
    Setup Grepzilla configuration and orchestration using YAML config-file.

    Args:
        path (Path): Path to the YAML configuration file.
    """

    pass

@app.command(
    name="init",
    help="Initialize Grepzilla configuration from Root file directory."
)
def init(
    path: Annotated[
        list[Path], 
        typer.Argument(
            help="Path/Paths to the Root file directory.", 
            prompt="Please enter filepath to one or more Root file directories.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
        )
    ]
):
    """
    Initialize Grepzilla configuration from Root file directory.

    Args:
        path (list[Path]): Path to the Root file directory.
    """

    pass

@app.command(
    name="query",
    help="Semantic query for relevant files and content."
)
def query():
    """
    Semantic query for relevant files and content.
    """

    pass

