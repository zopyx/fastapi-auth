from starlette.status import HTTP_200_OK
from .conftest import admin_username, admin_password


def test_login_form(user_management, test_client):
    response = test_client.get("/auth/login")
    assert response.status_code == HTTP_200_OK


def test_login_correct_credentials(user_management, test_client):
    response = test_client.post("/auth/login", data={"username": admin_username, "password": admin_password})
    assert response.status_code == HTTP_200_OK
    assert "now logged in" in response.text

    # Then, logout
    response = test_client.get("/auth/logout")
    assert response.status_code == HTTP_200_OK
    assert "been logged out" in response.text


def test_login_improper_credentials(user_management, test_client):
    response = test_client.post("/auth/login", data={"username": admin_username, "password": "wrong_password"})
    assert response.status_code == HTTP_200_OK
    import pdb

    pdb.set_trace()
    assert "" in response.text

    response = test_client.get("/auth/user-info")
    assert "Unauthorized" in response.text
