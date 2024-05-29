from pydantic import BaseModel, Field


from .roles import Role
from .permissions import Permission

from typeguard import typechecked


class User(BaseModel):
    """Users"""

    # Name of user
    name: str = Field(..., description="Name of the user")

    # Description of user
    description: str = Field(..., description="Description of the user")

    # Is user anonymous
    is_anonymous: bool = True

    # Roles of user
    roles: list[Role] = []

    # Properties of user
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
    def has_role_by_name(self, role_name: str) -> bool:
        """Check if the user has the required role (by name)."""
        for role in self.roles:
            if role.name == role_name:
                return True
        return False

    def role_names(self) -> list[str]:
        """Return a list of role names."""
        return [role.name for role in self.roles]

    def all_permissions(self) -> list[Permission]:
        """Return a list of all permissions."""
        permissions = []
        for role in self.roles:
            permissions.extend(role.permissions)
        return permissions

    def all_permission_names(self) -> list[str]:
        """Return a list of all permission names."""
        permissions = self.all_permissions()
        return [permission.name for permission in permissions]

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
