from typing import Literal

from datetime import date
from bson import ObjectId
from pydantic import BaseModel, Field

from core.schemas.utils import PyObjectId
from core.schemas.sheets import Sheet


class ModelMeta(BaseModel):
    name: str
    admins: list[PyObjectId]  # list of user_ids
    editors: list[PyObjectId]  # list of user_ids
    viewers: list[PyObjectId]  # list of user_ids
    workspace: PyObjectId  # workspace id
    starting_month: date


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
    id: str = Field(alias="_id")
    username: str
    first_name: str | None
    last_name: str | None
    user_role: Literal["Admin", "Editor", "Viewer"]
