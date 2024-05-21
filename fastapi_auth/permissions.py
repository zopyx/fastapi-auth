"""This module contains the Permission model."""

from pydantic import BaseModel, Field


class Permission(BaseModel):
    """A permission model."""

    name: str = Field(..., description="Name of the permission")
    description: str = Field(..., description="Description of the permission")
