import typer
from snowflake.cli.api.commands.snow_typer import SnowTyperFactory
from snowflake.cli.api.output.types import MessageResult

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
    return MessageResult(f"Hello, {name}! 👋")


@app.command(
    name="goodbye",
    requires_connection=False,
    requires_global_options=False,
)
def goodbye_command(
    name: str = typer.Option("John", "--name", "-n", help="Name to say goodbye to"),
) -> MessageResult:
    """
    Says goodbye to someone.
    """
    return MessageResult(f"Goodbye, {name}! 👋")
