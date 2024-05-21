"""Module for managing users in a SQLite database."""

import os
import sqlite3

import bcrypt

from typeguard import typechecked
from typing import Optional

from .logger import LOG
from .auth_config import AUTH_SETTINGS

LOG.info(f"Using database file {AUTH_SETTINGS.db_name}")


class UserManagement:
    """Class for managing users in a SQLite database."""

    @typechecked
    def __init__(self, db_filename: str) -> None:
        """Initialize the UserManagement instance."""
        self.db_filename = db_filename

    @property
    def connection(self) -> sqlite3.Connection:
        """Return the connection to the database."""
        if not os.path.exists(self.db_filename):
            msg = f"Database file {self.db_filename} does not exist."
            raise ValueError(msg)
        return sqlite3.connect(self.db_filename)

    @typechecked
    def delete_db(self) -> None:
        """Delete the database."""
        if os.path.exists(self.db_filename):
            os.remove(self.db_filename)

    @typechecked
    def create_db(self) -> None:
        """Create the database if it does not exist."""
        if not os.path.exists(self.db_filename):
            conn = sqlite3.connect(self.db_filename)
            c = conn.cursor()
            c.execute("""CREATE TABLE users
                        (username text primary key, password text, roles text)""")
            conn.commit()
            conn.close()

    @typechecked
    def has_user(self, username: str) -> bool:
        """Check if a user exists in the database."""
        conn = self.connection
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        return user is not None

    @typechecked
    def add_user(self, username: str, password: str, roles: str) -> None:
        """Add a user to the database."""
        if self.has_user(username):
            msg = f"User {username} already exists."
            raise ValueError(msg)
        conn = self.connection
        c = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, hashed_password, roles))
        conn.commit()
        conn.close()

    @typechecked
    def delete_user(self, username: str) -> None:
        """Delete a user from the database."""
        if not self.has_user(username):
            msg = f"User {username} does not exist."
            raise ValueError(msg)
        conn = self.connection
        c = conn.cursor()
        c.execute("DELETE from users WHERE username = ?", (username,))
        conn.commit()
        conn.close()

    @typechecked
    def change_password(self, username: str, password: str) -> None:
        """Change the password for a user."""
        if not self.has_user(username):
            msg = f"User {username} does not exist."
            raise ValueError(msg)
        conn = self.connection
        c = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
        conn.commit()
        conn.close()

    @typechecked
    def verify_password(self, username: str, password: str) -> bool:
        """Verify the password for a user."""

        if not self.has_user(username):
            msg = f"User {username} does not exist."
            raise ValueError(msg)

        conn = self.connection
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
        if row is None:
            return False
        return bcrypt.checkpw(password.encode(), row[0])

    @typechecked
    def get_user(self, username: str, password: str) -> Optional[dict]:
        """Validate user and password and return the user data as dict."""
        conn = self.connection
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()
        if row is None:
            return None
        if bcrypt.checkpw(password.encode(), row[1]):
            return {"username": row[0], "roles": row[2].split(",")}
        return None

    @typechecked
    def get_users(self) -> list:
        """List all users in the database."""

        conn = self.connection
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        conn.close()
        return rows
