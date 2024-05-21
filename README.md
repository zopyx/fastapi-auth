# fastapi-auth

An opionated authentication and authorization system for FastAPI.

## Features

- a SQLite-based user database (to be rewritten using SQLObject for broader database support)
- a commandline utility for adding, deleting users
- roles and permissions
- FastAPI endpoint protection based on permission or roles


## Status

- experimental

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

For now, `fastapi-auth` stores user accounts inside a Sqlite database. There is
the `fastapi-auth-user-admin` utility for managing user accounts through the
commandline.  There is no support (and there will be no support) for managing
user accounts through a web admin interface.

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

## Internals

The implementation is based on top of the `starlette-session`
(https://pypi.org/project/starlette-session/) middleware. The user information
is stored through a  signed cookie-based HTTP session. Session information is
readable but not modifiable. The encryption key can be configured through an environment
variable.


## Author

Andreas Jung <info@zopyx.com>

