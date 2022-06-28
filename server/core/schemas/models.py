from typing import Literal

from bson import ObjectId
from pydantic import BaseModel, Field

from core.objects import PyObjectId
from core.schemas.sheets import Sheet


class ModelMeta(BaseModel):
    name: str
    admins: list[str]  # list of usernames
    editors: list[str]  # list of usernames
    viewers: list[str]  # list of usernames
    workspace: str  # workspace name
    # todo what else?


class Model(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    meta: ModelMeta
    sheets: list[Sheet]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateModel(BaseModel):
    meta: ModelMeta
    sheets: list[Sheet]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ModelUser(BaseModel):
    username: str
    first_name: str | None
    last_name: str | None
    user_role: Literal["Admin", "Editor", "Viewer"]
