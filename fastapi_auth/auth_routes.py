from fastapi import Depends, Form, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from starlette.responses import HTMLResponse

from .dependencies import get_user
from .logger import LOG
from .users import User
from .user_management import UserManagement, USER_MANAGEMENT_SETTINGS
from .jinja2_templates import templates

from starlette.middleware.sessions import SessionMiddleware


SECRET_KEY = "my_secret_key2"

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
    print(user)

    if user_data is not None:
        request.session["username"] = user_data["username"]
        request.session["is_authenticated"] = True
        request.session["roles"] = user_data["roles"]
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


@router.get("/user-info", response_class=HTMLResponse)
async def user_info(
    request: Request,
    user: User = Depends(get_user),
):
    user_data = queries.get_user_information(deps.db, deps.user)
    message = request.query_params.get("message", None)
    return templates.TemplateResponse(
        "user_info.html", {"request": request, "user": deps.user, "message": message, "user_data": user_data}
    )
