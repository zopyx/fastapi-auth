"""This is a demo app to show how to use the fastapi_auth package."""

from typing import Optional

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from .auth_routes import router as auth_router, install_middleware
from .dependencies import get_user
from .users import User
from .jinja2_templates import templates
from .roles import ROLES_REGISTRY, Role
from .permissions import Permission
from .dependencies import Protected

# Your FastAPI app
app = FastAPI()
# install the session middleware
install_middleware(app)

# add endpoints for authentication examples
app.mount("/auth", auth_router)

# add static files (for demo login form)
app.mount("/static", StaticFiles(directory="static"), name="static")

# here, we define some permissions
VIEW_PERMISSION = Permission(
    name="view",
    description="View permission",
)
EDIT_PERMISSION = Permission(
    name="edit",
    description="Edit permission",
)
DELETE_PERMISSION = Permission(
    name="delete",
    description="Delete permission",
)

# and some roles that use these permissions
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

# The roles must be added to the global ROLES_REGISTRY
ROLES_REGISTRY.register(ADMIN_ROLE)
ROLES_REGISTRY.register(USER_ROLE)
ROLES_REGISTRY.register(VIEWER_ROLE)


# The default / endpoint uses the get_user dependency to get the current user,
# The "current user" is a User object that is stored in the session after
# authentication.  If the request is not authenticated, the ANONYMOUS_USER
# object is returned.  So, you will have `user` as an authenticated user or
# ANONYMOUS_USER as an unauthenticated user.


@app.get("/", response_class=HTMLResponse)
def read_root(
    request: Request,
    user: User = Depends(get_user),
    message: Optional[str] = None,
    error_message: Optional[str] = None,
):
    return templates.TemplateResponse(
        request,
        "demo.html",
        {"request": request, "user": user, "message": message, "error_message": error_message, },
    )


# This is an endpoint that requires the user to be authenticated.  In this case,
# the user must have the ADMIN_ROLE role.  It is also possible to require a
# permission instead.  Use the Protected dependency to require authentication.
# An unauthenticated request as ANONYMOUS_USER will be rejected.
@app.get("/admin")
def admin(user: User = Depends(Protected(required_roles=[ADMIN_ROLE]))):
    return {"user": user}


@app.get("/admin2")
def admin2(user: User = Depends(Protected(required_permission=VIEW_PERMISSION))):
    return {"user": user}
