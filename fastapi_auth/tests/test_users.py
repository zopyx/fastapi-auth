import pytest
from pydantic import ValidationError
from ..users import User
from ..roles import Role
from ..permissions import Permission


def test_user_creation():
    user = User(name="John Doe", description="Test user", is_anonymous=False)
    assert user.name == "John Doe"
    assert user.description == "Test user"
    assert not user.is_anonymous
    assert user.is_authenticated
    str(user)


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

    assert user.has_role_by_name("admin") == True
    assert user.has_role_by_name("user") == False


def test_role_names():
    perm1 = Permission(name="read", description="Read permission")
    perm2 = Permission(name="write", description="Write permission")
    roles = [
        Role(name="admin", description="Admin role", permissions=[perm1]),
        Role(name="user", description="User role", permissions=[perm2]),
    ]
    user = User(name="John Doe", description="Test user", roles=roles)
    assert user.role_names() == ["admin", "user"]
    assert list(user.all_permission_names()) == (["read", "write"])
