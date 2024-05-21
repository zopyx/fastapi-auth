"""Jinja2 templates for FastAPI."""

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader("fastapi_auth", "templates"))

# env.globals["format_iso8601_date"] = format_iso8601_date
# env.globals["format_iso8601_datetime"] = format_iso8601_datetime
# env.globals["format_float"] = format_float
# env.globals["get_permissions"] = get_user_permissions
templates = Jinja2Templates(env=env)
