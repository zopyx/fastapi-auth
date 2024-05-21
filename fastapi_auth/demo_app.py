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

app = FastAPI()
install_middleware(app)
app.mount("/auth", auth_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


VIEW_PERMISSION = Permission(name="view", description="View permission")
EDIT_PERMISSION = Permission(name="edit", description="Edit permission")
DELETE_PERMISSION = Permission(name="delete", description="Delete permission")

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

ROLES_REGISTRY.register(ADMIN_ROLE)
ROLES_REGISTRY.register(USER_ROLE)
ROLES_REGISTRY.register(VIEWER_ROLE)


@app.get("/", response_class=HTMLResponse)
def read_root(
    request: Request,
    user: User = Depends(get_user),
    message: str = None,
    error_message: str = None,
):
    return templates.TemplateResponse(
        "demo.html",
        {"request": request, "user": user, "message": message, "error_message": error_message},
    )


@app.get("/admin")
def admin(user: User = Depends(Protected(required_roles=[ADMIN_ROLE]))):
    return {"user": user}
