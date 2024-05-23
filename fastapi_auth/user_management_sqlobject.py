"""Module for managing users in a SQLite database."""

from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import datetime, timezone
from fastapi import Request
import bcrypt
from datetime import datetime, timedelta

from .auth_config import AUTH_SETTINGS
from .roles import ROLES_REGISTRY

LIFE_TIME = 3600 * 24

def utc_now():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    password: str
    roles: str
    created: datetime = Field(default_factory=utc_now)


class UserManagement:
    """Class for managing users in a SQL database."""

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


async def get_user_from_fastapi_request(request) -> User:
    """Get the user from a FastAPI request."""

    form = await request.form()
    username = form["username"]
    password = form["password"]

    um = UserManagement(AUTH_SETTINGS.db_uri)
    user_data = um.get_user(username, password)
    if not user_data:
        return None

    roles = user_data["roles"]
    roles = [ROLES_REGISTRY.get_role(r) for r in roles if ROLES_REGISTRY.has_role(r)]

    now = datetime.now(timezone.utc)
    expires = now + timedelta(seconds=LIFE_TIME)
    user = User(
        name=user_data["username"],
        description=user_data["username"],
        is_anonymous=False,
        roles=roles,
        properties=dict(
            source="internal",
            logged_in=now.isoformat(),
            expires=expires.isoformat(),
        ),
    )
    return user