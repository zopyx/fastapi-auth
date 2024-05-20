from typing import Optional

from fastapi import Depends, Request
from pydantic import BaseModel, ConfigDict

# from .user import User, get_user, Unauthorized

from .logger import LOG
from .users import User, ANOYMOUS_USER


def get_user(request: Request) -> User:
    """A dependency to get the dependencies."""
    print(request.session)

    session = request.session
    if "username" not in session:
        return ANOYMOUS_USER

    else:
        return User(
            name=session["username"],
            description=session["username"],
            is_anonymous=False,
            #        roles=session["roles"],
            roles=[],
        )
