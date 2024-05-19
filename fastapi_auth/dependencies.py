from typing import Optional

from fastapi import Depends
from pydantic import BaseModel, ConfigDict

from .user import User, get_user, Unauthorized, ALL_ROLES_LIST

from .logger import LOG


class MyDeps(BaseModel):
    """A class to hold dependencies."""

    user: Optional[User] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class MyDependencies:
    def __init__(self, required_permission: Optional[str] = None, required_roles: Optional[list | str] = None):
        if required_roles is None:
            required_roles = []
        if isinstance(required_roles, str):
            required_roles = [required_roles]

        if all([required_permission, required_roles]):
            raise ValueError("required_permission and required_role are mutual exclusive")

        if not required_permission and not required_roles:
            raise ValueError("Either required_permission or required_role must be given")

        self.required_permission = required_permission
        self.required_roles = required_roles

    def __call__(
        self,
        user: User = Depends(get_user),
        db=Depends(get_database),
    ) -> MyDeps:
        allowed = False
        for rr in self.required_roles:
            if user.role.name == rr:
                allowed = True
                break

        if self.required_permission and self.required_permission in user.role.permissions:
            allowed = True

        if allowed:
            return MyDeps(
                user=user,
                collection=collection,
                db=db,
            )

        msg = f"Permission denied for user {user}. Required roles: {self.required_roles}, required permission: {self.required_permission}. User has role {user.role} and permissions {user.role.permissions}"
        LOG.error(msg)
        raise Unauthorized(msg)


def get_deps(
    user: User = Depends(get_user),
    permission: str = "",
) -> MyDeps:
    """A dependency to get the dependencies."""

    return MyDeps(
        user=user,
    )
