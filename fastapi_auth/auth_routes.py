from typing import Optional

from fastapi import Depends, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status

from .dependencies import get_user
from .logger import LOG
from .users import User, ANONYMOUS_USER, SUPER_USER
from .roles import ROLES_REGISTRY
from .user_management_sqlobject import authenticate_user_for_fastapi
from .jinja2_templates import templates

from starlette.middleware.sessions import SessionMiddleware


from .auth_config import AUTH_SETTINGS

from .authenticator_registry import AUTHENTICATOR_REGISTRY

LIFE_TIME = 3600 * 24


router = APIRouter()


def install_middleware(app):
    app.add_middleware(SessionMiddleware, secret_key=AUTH_SETTINGS.secret_key.get_secret_value())


@router.get("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    user: User = Depends(get_user),
    message: Optional[str] = None,
    error_message: Optional[str] = None,
):
    return templates.TemplateResponse(
        request,
        "login.html",
        {
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
):
    if AUTH_SETTINGS.always_superuser:
        SUPER_USER.roles = ROLES_REGISTRY.all_roles()
        authenticate_user_for_fastapi(user=SUPER_USER, request=request)
        message = "You are now logged in as superuser."
        LOG.info(f"User {SUPER_USER.name} logged in")
        return RedirectResponse(f"/?message={message}", status_code=status.HTTP_302_FOUND)

    for authenticator in AUTHENTICATOR_REGISTRY.authenticators:
        LOG.debug(f"Trying to authenticate with {authenticator.name}")
        try:
            user = await authenticator.authenticate(request)
        except Exception as e:  # pragma: no cover
            LOG.error(f"Error authenticating with {authenticator.name}: {e}")
            user = None
        if user:
            break

    if user:
        authenticate_user_for_fastapi(user=user, request=request)
        message = f"Welcome {user.name}. You are now logged in."
        LOG.info(f"User {user.name} logged in")
        return RedirectResponse(f"/?message={message}", status_code=status.HTTP_302_FOUND)

    else:
        message = "You could not be logged in. Please try again."
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "user": ANONYMOUS_USER,
                "error_message": message,
            },
        )
