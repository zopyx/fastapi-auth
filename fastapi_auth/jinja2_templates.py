"""Jinja2 templates for FastAPI."""

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader("fastapi_auth", "templates"))

templates = Jinja2Templates(env=env)
