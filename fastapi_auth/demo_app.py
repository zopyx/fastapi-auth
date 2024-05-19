from fastapi import FastAPI
from starlette.responses import HTMLResponse

from .auth_routes import router as auth_router


app = FastAPI()
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <body>
            <h1>Welcome to our demo app!</h1>
            <a href="/login">Login</a>
            <br>
            <a href="/logout">Logout</a>
        </body>
    </html>
    """
