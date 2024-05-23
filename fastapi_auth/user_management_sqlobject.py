"""Module for managing users in a SQLite database."""

from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import datetime, timezone
import bcrypt
from rich.table import Table
from rich.console import Console


def utc_now():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    password: str
    roles: str
    created: datetime = Field(default_factory=utc_now)


class UserManagement:
    def __init__(self, db_uri) -> None:
        self.engine = create_engine(db_uri)
        SQLModel.metadata.create_all(self.engine)

    def add_user(self, username: str, password: str, roles: str) -> None:
        if self.has_user(username):
            raise ValueError(f"User {username} already exists.")
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(username=username, password=hashed_password, roles=roles)
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

    def delete_user(self, username: str) -> None:
        with Session(self.engine) as session:
            user = session.get(User, username)
            if user is None:
                raise ValueError(f"User {username} does not exist.")
            session.delete(user)
            session.commit()

    def get_user(self, username: str, password: str) -> dict:
        with Session(self.engine) as session:
            user = session.get(User, username)
            if user is None:
                return None
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return {"username": user.username, "roles": user.roles.split(",")}
            return None

    def get_users(self):
        with Session(self.engine) as session:
            return session.exec(select(User)).all()

    def has_user(self, username: str) -> bool:
        with Session(self.engine) as session:
            return session.get(User, username) is not None

    def change_password(self, username: str, new_password: str) -> None:
        with Session(self.engine) as session:
            user = session.get(User, username)
            if user is None:
                raise ValueError(f"User {username} does not exist.")
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            user.password = hashed_password
            session.add(user)
            session.commit()

    def verify_password(self, username: str, password: str) -> str:
        with Session(self.engine) as session:
            user = session.get(User, username)
            if user is None:
                raise ValueError(f"User {username} does not exist.")
            return bcrypt.checkpw(password.encode(), user.password.encode())


if __name__ == "__main__":
    um = UserManagement("sqlite:///xx.db")
    print("Adding user 'admin'...")
    um.add_user("admin", "password", "admin,user")
    print("Checking if user 'admin' exists...")
    print(um.has_user("admin"))  # Should print: True
    print("Getting user 'admin'...")
    print(um.get_user("admin", "password"))  # Should print: {'username': 'admin', 'roles': ['admin', 'user']}
    print("Getting all users...")
    print(um.get_users())  # Should print: [<User 1 username='admin' password='...' roles='admin,user' created='...'>]
    print("Changing password for user 'admin'...")
    um.change_password("admin", "new_password")
