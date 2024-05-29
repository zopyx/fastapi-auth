from fastapi import Request, Depends
from typing import Optional
from fastapi.exceptions import HTTPException
from typeguard import typechecked

# from .user import User, get_user, Unauthorized

from .users import User, ANONYMOUS_USER
from .roles import Role
from .permissions import Permission
from .logger import LOG


class Unauthorized(Exception):
    """ """


def get_user(request: Request) -> User:
    """This dependency return either an authenticated user depending on the
    presented token or an anonymous user if no token is presented."""

    if "user" not in request.session:
        return ANONYMOUS_USER
    return User(**request.session["user"])


class Protected:
    """A dependency to protect routes.  The user must have the required
    permission or a role to access the route.  Using a permission and role(s) are
    mutually exclusive. You must specify either a permission or a list of roles.
    This dependency should be used for authenticated routes only. only.  The
    authenticated user must either have a specified role or one of its role must
    support the required permission.
    """

    @typechecked
    def __init__(
        self,
        required_permission: Optional[Permission] = None,
        required_roles: Optional[list[Role]] = None,
    ):
        if required_roles is None:
            required_roles = []

        if all([required_permission, required_roles]):
            raise ValueError("required_permission and required_role are mutual exclusive")

        if not required_permission and not required_roles:
            raise ValueError("Either required_permission or required_role must be given")

        self.required_permission = required_permission
        self.required_roles = required_roles

    @typechecked
    def __call__(
        self,
        user: User = Depends(get_user),
    ) -> User:
        # check for roles
        for rr in self.required_roles:
            for user_role in user.roles:
                if user_role == rr:
                    return user

        # If the user has the required permission, return the user
        if self.required_permission:
            if user.has_permission(self.required_permission):
                return user

        msg = f"Permission denied for user {user}. Required roles: {self.required_roles}, required permission: {self.required_permission}. User has role {user.roles}"
        LOG.error(msg)
        raise HTTPException(status_code=403, detail=msg)
