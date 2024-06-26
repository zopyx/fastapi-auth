import pytest
from starlette.status import HTTP_200_OK
from .conftest import admin_username, admin_password

from ..dependencies import Protected
from ..roles import Role
from ..permissions import Permission
from ..auth_config import AUTH_SETTINGS


def test_Protected():
    perm = Permission(name="view", description="View")
    role = Role(name="foo", description="foo", permissions=[perm])

    with pytest.raises(ValueError):
        Protected(required_roles=[role], required_permission=perm)

    with pytest.raises(ValueError):
        Protected(required_roles=[], required_permission=None)


def test_protected_via_admin(user_management, test_client):
    test_client.get("/auth/logout")
    response = test_client.post("/auth/login", data={"username": admin_username, "password": admin_password})
    assert response.status_code == HTTP_200_OK

    response = test_client.get("/admin")
    assert response.status_code == HTTP_200_OK


def test_protected_via_admin2(user_management, test_client):
    test_client.get("/auth/logout")
    response = test_client.post("/auth/login", data={"username": admin_username, "password": admin_password})
    assert response.status_code == HTTP_200_OK

    response = test_client.get("/admin2")
    assert response.status_code == HTTP_200_OK


def test_protected_via_admin3(user_management, test_client):
    test_client.get("/auth/logout")
    response = test_client.post("/auth/login", data={"username": admin_username, "password": admin_password})
    assert response.status_code == HTTP_200_OK

    response = test_client.get("/admin3")
    assert response.status_code == HTTP_200_OK


def test_protected_via_admin_anonymous(user_management, test_client):
    test_client.get("/auth/logout")
    response = test_client.get("/admin")
    assert response.status_code == 403


def test_protected_via_admin2_anonymous(user_management, test_client):
    test_client.get("/auth/logout")
    response = test_client.get("/admin2")
    assert response.status_code == 403


def test_protected_via_admin3_anonymous(user_management, test_client):
    test_client.get("/auth/logout")
    response = test_client.get("/admin3")
    assert response.status_code == 403


def test_bypass_security(user_management, test_client):
    test_client.get("/auth/logout")

    AUTH_SETTINGS.always_superuser = True
    response = test_client.post("/auth/login", data={"username": admin_username, "password": admin_password})

    response = test_client.get("/admin")
    assert response.status_code == HTTP_200_OK
    AUTH_SETTINGS.always_superuser = False
