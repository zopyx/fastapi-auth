import pytest
from ..roles import Role, RolesRegistry
from ..permissions import Permission
from typeguard import TypeCheckError


from pydantic import ValidationError


def test_role_creation():
    role = Role(name="admin", description="Admin role")
    assert role.name == "admin"
    assert role.description == "Admin role"


def test_role_without_name():
    with pytest.raises(ValidationError):
        Role(description="Admin role")


def test_role_without_description():
    with pytest.raises(ValidationError):
        Role(name="admin")


def test_role_with_permissions():
    permissions = [
        Permission(name="read", description="Can read data"),
        Permission(name="write", description="Can write data"),
    ]
    role = Role(name="admin", description="Admin role", permissions=permissions)
    assert role.permissions == permissions


def test_role_creation2():
    perm1 = Permission(name="read", description="Read permission")
    perm2 = Permission(name="write", description="Write permission")
    role = Role(name="admin", description="Adminstrator role", permissions=[perm1, perm2])
    assert role.name == "admin"

    assert perm1 in role.permissions
    assert perm2 in role.permissions

    perm3 = Permission(name="delete", description="Delete permission")
    assert perm3 not in role.permissions


def test_role_registry():
    registry = RolesRegistry()
    READ = Permission(name="read", description="Read permission")
    WRITE = Permission(name="write", description="Write permission")
    role = Role(name="admin", description="admin", permissions=[READ, WRITE])
    registry.register(role)
    assert registry.get_role("admin") == role
    assert registry.has_role("admin") == True
    assert registry.all_roles() == [role]
    assert registry.all_role_names() == ["admin"]
    assert registry.admin == role
    assert registry.as_dict() == {"admin": role}
    with pytest.raises(ValueError):
        registry.get_role("user")
    with pytest.raises(TypeCheckError):
        registry.register("my_role")
