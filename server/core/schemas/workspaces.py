from typing import Literal

from bson import ObjectId
from pydantic import BaseModel, Field

from core.objects import PyObjectId


class Workspace(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    admin: PyObjectId
    users: list[PyObjectId]  # list of user_ids

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "62bb11835529faba0704639d",
                "name": "ACME Inc.",
                "admin": "62bb11835529faba0704639d",
                "users": [
                    "62bb11835529faba07046398",
                    "62bb11835529faba0704639b",
                    "62bb11835529faba0704639d",
                ],
            }
        }


class UpdateWorkspace(BaseModel):
    name: str | None
    admin: PyObjectId | None
    users: list[PyObjectId] | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "ACME Inc.",
                "admin": "62bb11835529faba0704639d",
                "users": [
                    "62bb11835529faba07046398",
                    "62bb11835529faba0704639b",
                    "62bb11835529faba0704639d",
                ],
            }
        }


class WorkspaceUser(BaseModel):
    id: str = Field(alias="_id")
    username: str
    first_name: str | None
    last_name: str | None
    user_role: Literal["Admin", "Member"]
