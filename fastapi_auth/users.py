from pydantic import BaseModel, Field


from .roles import Role
from .permissions import Permission

from typeguard import typechecked


class User(BaseModel):
    """Users"""

    name: str = Field(..., description="Name of the user")
    description: str = Field(..., description="Description of the user")
    is_anonymous: bool = True
    roles: list[Role] = []
    properties: dict = {}

    def __str__(self) -> str:
        """Return a string representation of the user."""
        self_str = super().__str__()
        return f"{self.__class__.__name__}({self_str})"

    @typechecked
    def has_role(self, role: Role) -> bool:
        """Check if the user has the required role."""
        return role in self.roles

    @typechecked
    def has_permission(self, permission: Permission) -> bool:
        """Check if the user has the required permission."""
        for role in self.roles:
            if permission in role.permissions:
                return True
        return False

    @property
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated."""
        return not self.is_anonymous


ANONYMOUS_USER = User(
    name="anonymous",
    description="Anonymous user",
    is_anonymous=True,
)
