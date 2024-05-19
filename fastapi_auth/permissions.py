from pydantic import BaseModel, Field


class Permission(BaseModel):
    name: str = Field(..., description="Name of the permission")
    description: str = Field(..., description="Description of the permission")
