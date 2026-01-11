from pathlib import Path

import typer
from snowflake.cli.api.commands.snow_typer import SnowTyperFactory
from snowflake.cli.api.output.types import CollectionResult, CommandResult, MessageResult

from snowflake_cli_devops.manager import FileManager

app = SnowTyperFactory(
    name="devops",
    help="Manages DevOps workflows with Snowflake.",
)


@app.command(
    name="greet",
    requires_connection=False,
    requires_global_options=False,
)
def greet_command(
    name: str = typer.Option("Jane", "--name", "-n", help="Name to greet"),
) -> MessageResult:
    """
    Says hello to someone.
    """
    return MessageResult(f"Hello, {name}!")

@app.command(
    name="list-projects",
    requires_connection=False,
    requires_global_options=True,
)
def list_projects_command(
    root_folder: Path = typer.Option(
        ...,
        "--root-folder",
        "-r",
        help="Root folder to search for Snowflake projects.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    **options,
) -> CommandResult:
    """
    Lists all Snowflake projects found in the specified root folder.

    A Snowflake project is identified by the presence of a snowflake.yml file.
    """
    manager = FileManager(root_folder=root_folder)
    projects = manager.list_projects()
    return CollectionResult(projects)
