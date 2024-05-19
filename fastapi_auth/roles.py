from pydantic import BaseModel, Field

from typeguard import typechecked

from .permissions import Permission


class Role(BaseModel):
    """Roles"""

    name: str = Field(..., description="Name of the role")
    description: str = Field(..., description="Description of the role")
    permissions: list[Permission] = []


class RolesRegistry:
    """Registry for roles."""

    def __init__(self):
        """Initialize the registry."""
        self.roles = dict()

    @typechecked
    def register(self, role: "Role") -> None:
        """Register a role."""
        self.roles[role.name] = role

    @typechecked
    def all_roles(self) -> list[Role]:
        """Return all roles."""
        return [r for r in self.roles.values()]

    @typechecked
    def all_role_names(self) -> list[str]:
        """Return all role names."""
        return list(self.roles.keys())

    @typechecked
    def get_role(self, role_name: str) -> "Role":
        """Get a role by name."""
        try:
            return self.roles[role_name]
        except KeyError:
            raise ValueError(f"Role {role_name} not found in role registry")

    @typechecked
    def has_role(self, role_name: str) -> bool:
        """Check if the registry has a role."""
        return role_name in self.roles

    @typechecked
    def __getattr__(self, role_name: str):
        """Get a role by name."""
        if role_name in self.roles:
            return self.roles[role_name]
        raise ValueError(f"Role {role_name} not found in role registry")

    @typechecked
    def as_dict(self) -> dict[str, "Role"]:
        """Return the roles as a dictionary."""
        return self.roles
