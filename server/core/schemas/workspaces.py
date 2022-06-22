from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from core.models.objects import PyObjectId


class Workspace(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    admin: EmailStr
    users: list[EmailStr]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "admin": "jdoe@example.com",
                "users": [
                    "alice@me.com",
                    "bob@me.com",
                    "jdoe@example.com"
                ]
            }
        }


class UpdateWorkspace(BaseModel):
    name: str | None
    admin: EmailStr| None
    users: list[EmailStr] | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "admin": "jdoe@example.com",
                "users": [
                    "alice@me.com",
                    "bob@me.com",
                    "jdoe@example.com"
                ]
            }
        }