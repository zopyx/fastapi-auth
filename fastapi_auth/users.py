from pydantic import BaseModel, Field


from .roles import Role


from typeguard import typechecked


class User(BaseModel):
    """Users"""

    name: str = Field(..., description="Name of the user")
    description: str = Field(..., description="Description of the user")
    is_anonymous: bool = True
    roles: list[Role] = []

    def __str__(self) -> str:
        """Return a string representation of the user."""
        self_str = super().__str__()
        return f"{self.__class__.__name__}({self_str})"

    @typechecked
    def has_role(self, role: Role) -> bool:
        """Check if the user has the required role."""
        return role in self.roles
