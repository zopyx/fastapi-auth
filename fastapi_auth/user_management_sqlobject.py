"""Module for managing users in a SQLite database."""

from sqlobject import SQLObject, StringCol, DateTimeCol, sqlhub, connectionForURI
from datetime import datetime
from sqlobject.main import SQLObjectNotFound
import bcrypt


class User(SQLObject):
    username = StringCol(alternateID=True)
    password = StringCol()
    roles = StringCol()
    created = DateTimeCol(default=datetime.utcnow)


class UserManagement:
    def __init__(self, db_uri):
        sqlhub.processConnection = connectionForURI(db_uri)
        User.createTable(ifNotExists=True)

    def add_user(self, username: str, password: str, roles: str):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        User(username=username, password=hashed_password.decode(), roles=roles)

    def delete_user(self, username: str):
        if not User.byUsername(username):
            raise ValueError(f"User {username} does not exist.")
        user = User.byUsername(username)
        user.destroySelf()

    def get_user(self, username: str, password: str):
        if not User.byUsername(username):
            return None
        user = User.byUsername(username)
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            return {"username": user.username, "roles": user.roles.split(",")}
        return None

    def get_users(self):
        return list(User.select())

    def has_user(self, username: str):
        try:
            User.byUsername(username)
            return True
        except SQLObjectNotFound:
            return False

    def change_password(self, username: str, new_password: str):
        user = User.byUsername(username)
        if user is None:
            raise ValueError(f"User {username} does not exist.")
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        user.password = hashed_password.decode()

    def verify_password(self, username: str, password: str):
        user = User.byUsername(username)
        if user is None:
            raise ValueError(f"User {username} does not exist.")
        return bcrypt.checkpw(password.encode(), user.password.encode())


if __name__ == "__main__":
    um = UserManagement("sqlite:/:memory:")
    print("Adding user 'admin'...")
    um.add_user("admin", "password", "admin,user")
    print("Checking if user 'admin' exists...")
    print(um.has_user("admin"))  # Should print: True
    print("Getting user 'admin'...")
    print(um.get_user("admin", "password"))  # Should print: {'username': 'admin', 'roles': ['admin', 'user']}
    print("Getting all users...")
    print(um.get_users())  # Should print: [<User 1 username='admin' password='...' roles='admin,user' created='...'>]
    print("Changing password for user 'admin'...")
    um.change_password("admin", "new_password")
    print("Verifying password for user 'admin'...")
    print(um.verify_password("admin", "new_password"))  # Should print: True
    print("Deleting user 'admin'...")
    um.delete_user("admin")
    print("Checking if user 'admin' exists...")
    print(um.has_user("admin"))  # Should print: False
