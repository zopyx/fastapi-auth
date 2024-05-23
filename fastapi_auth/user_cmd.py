"""Command line interface for user management."""

import typer

from .logger import LOG
from .auth_config import AUTH_SETTINGS
from rich.table import Table
from rich.console import Console


# from .user_management import UserManagement
from .user_management_sqlobject import UserManagement


app = typer.Typer()


def get_user_management() -> UserManagement:
    """Get a UserManagement instance."""
    LOG.debug(f"Using database {AUTH_SETTINGS.db_uri}")
    return UserManagement(AUTH_SETTINGS.db_uri)


@app.command()
def add(username: str, password: str, roles: str) -> None:
    """Add a user to the database."""
    um = get_user_management()
    um.add_user(username, password, roles)
    LOG.debug(f"Added user {username} with roles {roles}")


@app.command()
def delete(user: str) -> None:
    """Delete a user from the database."""
    um = get_user_management()
    um.delete_user(user)
    LOG.debug(f"Deleted user {user}")


@app.command()
def set_password(user: str, password: str) -> None:
    """Set the password for a user."""
    um = get_user_management()
    um.change_password(user, password)
    LOG.debug(f"Changed password for user {user}")


@app.command()
def verify_password(user: str, password: str) -> None:
    """Verify the password for a user."""
    um = get_user_management()
    if um.verify_password(user, password):
        typer.echo("Password is correct.")
    else:
        typer.echo("Password is incorrect.")


@app.command()
def list_users() -> None:
    """List all users in the database."""
    um = get_user_management()
    users = um.get_users()

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Role")
    table.add_column("Created")
    for user in users:
        table.add_row(user.username, user.roles, user.created.isoformat())
    console.print(table)
