# zopyx-fastapi-auth

An opionated authentication and authorization system for FastAPI.

## Features

- a RDBMS-based user database (support for almost all databases through sqlmodel)
- a commandline utility for adding, deleting users
- roles and permissions
- FastAPI endpoint protection based on permission or roles
- fully tested, full test coverage, full mypy compliance, parameter checks at runtime
- a plugin system for arbitrary authentication/authorization (requires one class and one method to implement)

![Tests](https://github.com/zopyx/fastapi-auth/actions/workflows/python-app.yml/badge.svg)

## Status

- in production

## Requirements

- supports Python 3.10-3.12 (no support for Python 3.9 or lower, no support for Python 3.13 yet)

## Example usage

- see `demo_app.py`

## Concepts

This package is build around the following concepts:

### Roles and permissions

A role is assigned to a user. A user can have one or more roles.  A permission
defines a certain certain access scope like `View entries`, `Delete entries`,
`Update Entries`. A Role can be have multiple permissions. So a  user can have
multiple roles and one role can have multiple permissions.

Example on how to define permissions:

```
from fastapi_auth.permissions import Permission

VIEW_PERMISSION = Permission(name="view", description="View permission")
EDIT_PERMISSION = Permission(name="edit", description="Edit permission")
DELETE_PERMISSION = Permission(name="delete", description="Delete permission")
```

Roles are defined this way:

```
from fastapi_auth.permissions import  Role

ADMIN_ROLE = Role(
    name="Administrator",
    description="Admin role",
    permissions=[VIEW_PERMISSION, EDIT_PERMISSION, DELETE_PERMISSION],
)
USER_ROLE = Role(
    name="User",
    description="User role",
    permissions=[VIEW_PERMISSION, EDIT_PERMISSION],
)
VIEWER_ROLE = Role(
    name="Viewer",
    description="Viewer role",
    permissions=[VIEW_PERMISSION],
)
```

Also, all roles must be registered with a global `ROLES_REGISTRY`:

```

from fastapi_auth.roles import ROLES_REGISTRY

ROLES_REGISTRY.register(ADMIN_ROLE)
ROLES_REGISTRY.register(USER_ROLE)
ROLES_REGISTRY.register(VIEWER_ROLE)
```


An endpoint of a FastAPI application be protected through one permission or one
or more roles.

In this example, the `/admin` endpoint is only acceessible for an authenticated user with role `Administrator`:

```
# This is an endpoint that requires the user to be authenticated.  In this case,
# the user must have the ADMIN_ROLE role.  It is also possible to require a
# permission instead.  Use the Protected dependency to require authentication.
# An unauthenticated request as ANONYMOUS_USER will be rejected.
@app.get("/admin")
def admin(user: User = Depends(Protected(required_roles=[ADMIN_ROLE]))):
    return {"user": user}
```

You could also protect an endpoint using a permission:

```

from fastapi_auth.dependencies import Protected

@app.get("/admin")
def admin2(user: User = Depends(Protected(required_permission=VIEW_PERMISSION))):
    return {"user": user}

```

Another option is to protect a route with a custom callback method returning `True` or `False` for a given
`Request` and `User`:

```
from fastapi_auth.dependencies import Protected

def my_check(request: Request, user: User) -> bool:
    # perform some checks based on request and/or user....
    return True # or False

@app.get("/admin")
def admin3(user: User = Depends(Protected(required_checker=my_check))):
    return {"user": user}
```

Note that the `user` object passed to the callback is either an already
authenticated users or the `ANONYMOUS_USER`.  It is up to the callback to
authorize the already authenticated user based on further criteria.



## Installation of the session middleware

In order to instrumentize your application, you need call `install_middleware(app)` with your
custom FastAPI `app` object.

```
from fastapi_auth.auth_routes import install_middleware

# Your FastAPI app
app = FastAPI()

# install the session middleware
install_middleware(app)

# add endpoints for authentication examples
app.mount("/auth", auth_router)

# add static files (for demo login form)
app.mount("/static", StaticFiles(directory="static"), name="static")
```

## User management

For now, `fastapi-auth` stores user accounts inside a SQL database. There is
the `fastapi-auth-user-admin` utility for managing user accounts through the
commandline.  There is no support (and there will be no support) for managing
user accounts through a web admin interface. The database connection can be configured
using the `AUTH_DB_URI` environment variable.

### adding user

```
fastapi-auth-user-admin add <username> <password> "Role1,Role2..."
```

### delete user

```
fastapi-auth-user-admin delete <username>
```

### list users

```
fastapi-auth-user-admin list-users 
```

### set password users

```
fastapi-auth-user-admin set-password <username> <new-password> 
```

## Environment variables

### AUTH_DEFAULT_KEY

`AUTH_DEFAULT_KEY` is used as encryption key for the user's session information.
It is strongly recommended to set this value rather than depending on the
default key as used in the code.

### AUTH_DB_URI

`AUTH_DB_URI` must be set to a SQL database. `zopyx-fastapi-auth` uses
`sqlmodel` under the hood which uses `SQLAlchemy`and all supported databases
(see https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls). 

Example for using a SQLite database `users.db` inside the current working directory:

```
export AUTH_DB_URI=sqlite:///users.db
```

### AUTH_LOG_FILENAME

By default, the module logs output to the console and to the `fastpi_auth.log`.
You can use a different filename by setting the `AUTH_LOG_FILENAME` environment
variable.

## Internals

The implementation is based on top of the `starlette-session`
(https://pypi.org/project/starlette-session/) middleware. The user information
is stored through a  signed cookie-based HTTP session. Session information is
readable but not modifiable. The encryption key can be configured through an environment
variable.

## Getting started with the included mini demo application

### Installation

Checkout the codebase and install it using pip or uv:

```
python3.12 -m venv .venv
source .venv/bin/activate
pip3 install -e .
```

or
```
uv venv -p python3.12
source .venv/bin/activate
uv pip install -e .
```

### Create a demo user

```
fastapi-auth-user-admin add admin admin Administrator
```
This will create a user `admin` with password `admin`.

### Running the demo service

```
uvicorn fastapi_auth.demo_app:app
```

### Login into the demo application

Visit http://localhost:8000/auth/login and login as `admin`/`admin`.

![Login into application](/images/login.png)

### After successfull login

![Login into application](/images/logged-in.png)


## Pluggable authenticators

This module provides a flexible architecture that allows the use of multiple
authentication and authorization backends within your FastAPI application. For
instance, you can configure the authentication system to use the default
Relational Database Management System (RDBMS)-based user management,
supplemented with an additional plugin for Lightweight Directory Access Protocol
(LDAP).

### Example

An `Authenticator` is required to implement an `authenticate(request: Request)`
method. This method should extract the login parameters from a login request and
return a `Users` object. Authenticators need to be registered with the
`AUTHENTICATOR_REGISTRY`. The execution order of the Authenticators is
determined by their `position` parameter. A `position` of `0` indicates that the
Authenticator is the first to be used. A higher `position` value signifies a
lower priority.

```
from fastapi import Request
from fastapi.authenticator_registry import Authenticator, AUTHENTICATOR_REGISTRY
from fastapi.users import User 

class MyAuthenticator(Authenticator):

    async def authenticate(request: Request) -> User:

        # extract credentials from request
        username = request.form....
        password = request.form....

        # perform authentication against your own authentication system
        user_data = my_backend.authenticate_user(username, password)
        
        return User(name=user_data["name"], roles=[...])

AUTHENTICATOR_REGISTRY.add_authenticator(MyAuthenticator(), 0)
```

## Provided routes

The `demo_app.py` application demonstrates the integration of `/auth/login` and
`/auth/logout` routes. You can find the implementation of these routes in
`auth_routes.py`. This code is customizable, allowing you to adapt it to your
specific requirements, as it includes some pre-configured decisions related to
logging and UI integration. The essence of the login process resides in the
`login_post()` function. Given its simplicity and brevity, you should find it
straightforward to tailor the login procedure to your needs.

## Author

Andreas Jung <info@zopyx.com>
