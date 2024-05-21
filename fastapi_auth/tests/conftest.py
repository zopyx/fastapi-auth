from fastapi.testclient import TestClient
from kataster.app import app
import pytest
from ..user_management import UserManagement
import tempfile


admin_username = "test_user"
admin_password = "test_password"


@pytest.fixture(scope="module")
def user_management():
    # Ensure that the user management instance is initialized with a temporary database
    def my_init(self, db_name):
        self.db_filename = temp_db_filename

    old_init = UserManagement.__init__
    UserManagement.__init__ = my_init

    temp_db_filename = tempfile.mktemp(suffix=".db")
    um = UserManagement(temp_db_filename)
    um.create_db()
    um.add_user(admin_username, admin_password, "Administrator")
    um.add_user("adhei", "adhei", "Kunde")
    um.add_user("fire", "fire", "Feuerwehr")
    um.add_user("admin", "admin", "Administrator")
    yield um
    UserManagement.__init__ = old_init
    um.delete_db()


@pytest.fixture(scope="module")
def test_client():
    yield TestClient(app)
