"""Jinja2 templates for FastAPI."""

from datetime import datetime

from typeguard import typechecked

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, PackageLoader

from .user import User, KatasterUser


@typechecked
def format_iso8601_date(date_str: str) -> str:
    """Format an ISO8601 date string to a human-readable date string."""
    return datetime.fromisoformat(date_str).strftime("%d.%m.%Y")


@typechecked
def format_iso8601_datetime(date_str: str) -> str:
    """Format an ISO8601 datetime string to a human-readable datetime string."""
    return datetime.fromisoformat(date_str).strftime("%d.%m.%Y %H:%M:%S")


@typechecked
def format_float(value: float) -> str:
    # format a float to three digits, with comma separator
    return "{:_.3f}".format(value).replace(".", ",")


def get_user_permissions(user: User) -> list:
    """Get the permissions of a user."""
    try:
        return user.role.permissions
    except Exception:
        return []


env = Environment(loader=PackageLoader("kataster", "templates"))

env.globals["format_iso8601_date"] = format_iso8601_date
env.globals["format_iso8601_datetime"] = format_iso8601_datetime
env.globals["format_float"] = format_float
env.globals["get_permissions"] = get_user_permissions
templates = Jinja2Templates(env=env)
