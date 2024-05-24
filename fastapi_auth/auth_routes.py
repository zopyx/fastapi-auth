from typing import Optional

from fastapi import Depends, Form, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status

from .dependencies import get_user
from .logger import LOG
from .users import User, ANONYMOUS_USER
from .user_management_sqlobject import get_user_from_fastapi_request, authenticate_user_for_fastapi
from .jinja2_templates import templates

from starlette.middleware.sessions import SessionMiddleware

from .auth_config import AUTH_SETTINGS

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
    username: str = Form(...),
    password: str = Form(...),
):
    user = await get_user_from_fastapi_request(request)

    if user:
        authenticate_user_for_fastapi(user=user, request=request)
        message = f"Welcome {user.name}. You are now logged in."
        LOG.info(f"User {user.name} logged in")
        return RedirectResponse(f"/?message={message}", status_code=status.HTTP_302_FOUND)

    else:
        message = "You could not be logged in. Please try again."
        LOG.error(message)
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "user": ANONYMOUS_USER,
                "error_message": message,
            },
        )
