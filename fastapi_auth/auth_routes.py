from fastapi import Depends, Form, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from starlette.responses import HTMLResponse

from ..dependencies import MyDeps, get_deps, get_database, DependencyAllRoles
from ..logger import LOG
from ..user import User, authenticate_user
from ..jinja2_templates import templates
from ..arangodb import get_users_collection, get_database

from .. import queries


SECRET_KEY = "my_secret_key2"

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    deps: MyDeps = Depends(get_deps),
):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "user": deps.user},
    )


@router.get("/logout")
async def logout(
    request: Request,
    deps: MyDeps = Depends(DependencyAllRoles),
):
    request.session.clear()
    message = "Sie wurden abgemeldet."
    return RedirectResponse(url=f"/?message={message}")


@router.post("/login")
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    deps: MyDeps = Depends(get_deps),
):
    user: User = authenticate_user(
        username=username,
        password=password,
    )

    # Ensure that the users collection exists
    db = get_database()
    get_users_collection(db)

    # Add your authentication logic here
    if not user.is_anonymous:
        request.session["username"] = user.id
        request.session["is_authenticated"] = True
        request.session["role"] = user.role.name
        message = f"Willkommen {user.name}. Sie sind jetzt angemeldet."
        LOG.info(f"User {user.id} logged in")

        return RedirectResponse(f"/?message={message}", status_code=status.HTTP_302_FOUND)

    message = "Keine Zugangsberechtigung oder falsche Zugangsdaten."
    LOG.error(f"User {user.id} unable to login")
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "user": user,
            "error_message": message,
        },
    )


@router.get("/user-info", response_class=HTMLResponse)
async def user_info(
    request: Request,
    deps: MyDeps = Depends(DependencyAllRoles),
):
    user_data = queries.get_user_information(deps.db, deps.user)
    message = request.query_params.get("message", None)
    return templates.TemplateResponse(
        "user_info.html", {"request": request, "user": deps.user, "message": message, "user_data": user_data}
    )


@router.post("/update-user-info")
async def update_user_info(
    request: Request,
    abschreibung: str = Form(...),
    deps: MyDeps = Depends(DependencyAllRoles),
):
    if deps.user.is_anonymous:
        message = "Sie sind nicht angemeldet."
        return RedirectResponse(f"/?message={message}", status_code=status.HTTP_302_FOUND)

    queries.update_user_abschreibung(db=deps.db, user=deps.user, abschreibung=abschreibung)

    message = "Ihre Daten wurden aktualisiert."
    return RedirectResponse(f"/auth/user-info?message={message}", status_code=status.HTTP_302_FOUND)
