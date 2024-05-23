from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel, Field, Session, create_engine, select
from ..user_management_sqlobject import UserManagement
import tempfile
import uuid

from ..demo_app import app


admin_username = "admin"
admin_password = "admin"


@pytest.fixture(scope="module")
def user_management():
    # Ensure that the user management instance is initialized with a temporary database
    def my_init(self, db_uri):
        self.engine = create_engine(tmp_db_uri)
        SQLModel.metadata.create_all(self.engine)

    old_init = UserManagement.__init__
    UserManagement.__init__ = my_init

    tmp_db = str(uuid.uuid4()) + ".db"
    tmp_db_uri = f"sqlite:///{tmp_db}"
    um = UserManagement(tmp_db)
    um.add_user("admin", "admin", "Administrator")
    yield um
    UserManagement.__init__ = old_init


@pytest.fixture(scope="module")
def test_client():
    yield TestClient(app)
