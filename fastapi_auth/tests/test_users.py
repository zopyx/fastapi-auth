import pytest
from pydantic import ValidationError
from ..users import User
from ..roles import Role


def test_user_creation():
    user = User(name="John Doe", description="Test user")
    assert user.name == "John Doe"
    assert user.description == "Test user"


def test_user_without_name():
    with pytest.raises(ValidationError):
        User(description="Test user")


def test_user_without_description():
    with pytest.raises(ValidationError):
        User(name="John Doe")


def test_user_with_roles():
    roles = [Role(name="admin", description="Admin role"), Role(name="user", description="User role")]
    user = User(name="John Doe", description="Test user", roles=roles)
    assert user.roles == roles


def test_has_role():
    role = Role(name="admin", description="Admin role")
    user = User(name="John Doe", description="Test user", roles=[role])
    assert user.has_role(role) == True
    assert user.has_role(Role(name="user", description="User role")) == False
