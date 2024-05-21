from fastapi import Depends, Form, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from datetime import timedelta

from .dependencies import get_user
from .logger import LOG
from .users import User
from .user_management import UserManagement, USER_MANAGEMENT_SETTINGS
from .jinja2_templates import templates
from .roles import ROLES_REGISTRY
from datetime import datetime, timezone

from starlette.middleware.sessions import SessionMiddleware


SECRET_KEY = "my_secret_key2"
LIFE_TIME = 3600 * 24


router = APIRouter()


def install_middleware(app):
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@router.get("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    user: User = Depends(get_user),
    message: str = None,
    error_message: str = None,
):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "user": user,
            "message": message,
            "error_message": error_message,
        },
    )


@router.get("/logout")
async def logout(
    request: Request,
    user: User = Depends(get_user),
):
    request.session.clear()
    message = "You have been logged out."
    return RedirectResponse(url=f"/?message={message}")


@router.post("/login")
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    user: User = Depends(get_user),
):
    um = UserManagement(USER_MANAGEMENT_SETTINGS.db_filename)
    user_data = um.get_user(username, password)

    if user_data is not None:
        roles = user_data["roles"]
        roles = [ROLES_REGISTRY.get_role(r) for r in roles if ROLES_REGISTRY.has_role(r)]

        now = datetime.now(timezone.utc)
        expires = now + timedelta(seconds=LIFE_TIME)
        user = User(
            name=user_data["username"],
            description=user_data["username"],
            is_anonymous=False,
            roles=roles,
            properties=dict(
                source="internal",
                logged_in=now.isoformat(),
                expires=expires.isoformat(),
            ),
        )
        request.session["user"] = user.model_dump()
        message = f"Welcome {user_data['username']}. You are now logged in."
        LOG.info(f"User {user_data['username']} logged in")
        return RedirectResponse(f"/?message={message}", status_code=status.HTTP_302_FOUND)

    else:
        message = f"You {username} could not be logged in. Please try again."
        LOG.error(message)
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error_message": message,
            },
        )
