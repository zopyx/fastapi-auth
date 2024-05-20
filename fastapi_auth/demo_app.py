from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from .auth_routes import router as auth_router, install_middleware
from .dependencies import get_user
from .users import User
from .jinja2_templates import templates

app = FastAPI()
install_middleware(app)
app.mount("/auth", auth_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


from . import user_management


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
