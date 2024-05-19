"""Command line interface for user management."""

import os

import typer
from pydantic_settings import BaseSettings

from kataster.logger import LOG
from kataster.user import ROLES_REGISTRY
from kataster.user_management import UserManagement

DEFAULT_DB_FILENAME = os.path.abspath("user_management.db")


class UserManagementSettings(BaseSettings):
    """Settings for the user management."""

    db_filename: str = DEFAULT_DB_FILENAME


app = typer.Typer()


def get_user_management() -> UserManagement:
    """Get a UserManagement instance."""
    user_management_settings = UserManagementSettings()
    LOG.debug(f"Using database file {user_management_settings.db_filename}")
    return UserManagement(user_management_settings.db_filename)


@app.command()
def add(username: str, password: str, roles: str) -> None:
    """Add a user to the database."""
    um = get_user_management()
    um.create_db()

    roles_lst = roles.split(",")
    allowed_roles = ROLES_REGISTRY.all_role_names()
    if not all(role in allowed_roles for role in roles_lst):
        msg = f"Invalid roles: {roles}"
        raise ValueError(msg)

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
    for user in users:
        typer.echo(user)


@app.command()
def delete_db() -> None:
    """Delete the database."""
    um = get_user_management()
    um.delete_db()
    LOG.debug("Deleted the database.")


def main() -> None:
    """Run the application."""
    app()


if __name__ == "__main__":
    app()
