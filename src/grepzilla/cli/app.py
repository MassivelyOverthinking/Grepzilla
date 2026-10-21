# ------------------------------------------------------------------------------------------------------------------------
# IMPORTS & MODULES
# ------------------------------------------------------------------------------------------------------------------------

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .callback import validate_config_file

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
        str, 
        typer.Argument(
            help="Path to the YAML configuration file.", 
            prompt="Please enter filepath to YAML config-file.",
            callback=validate_config_file
        )
    ],
):
    """
    Setup Grepzilla configuration and orchestration using YAML config-file.

    Args:
        path (str): Path to the YAML configuration file.
    """

    pass

