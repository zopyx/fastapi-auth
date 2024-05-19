import pytest

from ..permissions import Permission

from pydantic import ValidationError


def test_permission_creation():
    permission = Permission(name="read", description="Can read data")
    assert permission.name == "read"
    assert permission.description == "Can read data"


def test_permission_without_name():
    with pytest.raises(ValidationError):
        permission = Permission(description="Can read data")


def test_permission_without_description():
    with pytest.raises(ValidationError):
        permission = Permission(name="read")
