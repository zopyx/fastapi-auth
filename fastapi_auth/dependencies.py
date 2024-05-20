from typing import Optional

from fastapi import Depends, Request
from pydantic import BaseModel, ConfigDict

# from .user import User, get_user, Unauthorized

from .logger import LOG
from .users import User, ANOYMOUS_USER


def get_user(request: Request) -> User:
    """A dependency to get the dependencies."""
    if "user" not in request.session:
        return ANOYMOUS_USER
    return User(**request.session["user"])
