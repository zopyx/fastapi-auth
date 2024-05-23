import unittest
from ..user_management_sqlobject import UserManagement

import os
import pytest


class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.db_temp = "xx.db"
        self.um = UserManagement(f"sqlite:///{self.db_temp}")

    def tearDown(self):
        os.unlink(self.db_temp)

    def test_add_user(self):
        self.um.add_user("admin", "password", "admin,user")
        self.assertTrue(self.um.has_user("admin"))

    def test_add_user_twice(self):
        self.um.add_user("admin", "password", "admin,user")
        with pytest.raises(ValueError):
            self.um.add_user("admin", "password", "admin,user")

    def test_delete_user(self):
        self.um.add_user("admin", "password", "admin,user")
        self.um.delete_user("admin")
        self.assertFalse(self.um.has_user("admin"))

    def test_delete_non_existing_user(self):
        with pytest.raises(ValueError):
            self.um.delete_user("admin")

    def test_get_user(self):
        self.um.add_user("admin", "password", "admin,user")
        user = self.um.get_user("admin", "password")
        self.assertEqual(user, {"username": "admin", "roles": ["admin", "user"]})

    def test_get_non_existing_user(self):
        user = self.um.get_user("admin", "password")
        self.assertIsNone(user)

    def test_get_users(self):
        self.um.add_user("admin", "password", "admin,user")
        users = self.um.get_users()
        self.assertEqual(len(users), 1)

    def test_has_user(self):
        self.um.add_user("admin", "password", "admin,user")
        self.assertTrue(self.um.has_user("admin"))

    def test_change_password(self):
        self.um.add_user("admin", "password", "admin,user")
        self.um.change_password("admin", "new_password")
        user = self.um.get_user("admin", "new_password")
        self.assertEqual(user, {"username": "admin", "roles": ["admin", "user"]})

    def test_change_password_non_existing_user(self):
        with pytest.raises(ValueError):
            self.um.change_password("admin", "new_password")

    def test_verify_password(self):
        self.um.add_user("admin", "password", "admin,user")
        self.assertTrue(self.um.verify_password("admin", "password"))

    def test_verify_password_non_existing_user(self):
        with pytest.raises(ValueError):
            self.um.verify_password("admin", "password")
