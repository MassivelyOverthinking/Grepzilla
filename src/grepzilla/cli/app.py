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

# Setup Command ==> USe YAML config-file to setup the Grepzilla behaviour.
# Overwrites existing configuration and orchestration settings.
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
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite",
            "-o",
            help="Overwrite existing configuration and orchestration settings.",
            is_flag=True,
        )
    ]
):
    """
    Setup Grepzilla configuration and orchestration using YAML config-file.

    Args:
        path (Path): Path to the YAML configuration file.
        overwrite (bool): Whether to overwrite existing configuration and orchestration settings.
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
def query(
    query: Annotated[
        str,
        typer.Argument(
            help="Semantic query for relevant files and content.",
            min_length=1,
        )
    ],
    number: Annotated[
        int,
        typer.Option(
            "--number",
            "-n",
            help="Number of relevant files to return.",
            min=1,
            max=100,
            default=10,
            show_default=True,
        )
    ],
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Enable verbose output.",
            is_flag=True,
        )
    ]
):
    """
    Semantic query for relevant files and content.
    """

    pass

@app.command(
    name="root",
    help="View, add or remove Grepzilla Root file directories."
)
def root():
    pass

@app.command(
    name="report",
    help="View the current Grepzilla configuration and orchestration report."
)
def report():
    """
    View the current Grepzilla configuration and orchestration report.
    """
    
    pass

@app.command(
    name="history",
    help="View the history of previous queries and results."
)
def history():
    """
    View the history of previous queries and results.
    """

    pass
