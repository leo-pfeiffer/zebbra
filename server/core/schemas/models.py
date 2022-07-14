import uuid
from typing import Literal

from datetime import date
from bson import ObjectId
from pydantic import BaseModel, Field

from core.schemas.integrations import IntegrationProvider
from core.schemas.utils import PyObjectId, DateString
from core.schemas.sheets import Sheet


class ModelMeta(BaseModel):
    name: str
    admins: list[PyObjectId]  # list of user_ids
    editors: list[PyObjectId]  # list of user_ids
    viewers: list[PyObjectId]  # list of user_ids
    workspace: PyObjectId  # workspace id
    starting_month: date

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Employee(BaseModel):
    id: str = Field(default_factory=lambda: str(int(uuid.uuid4())), alias="_id")
    name: str
    start_date: DateString
    end_date: DateString | None
    title: str
    department: str
    monthly_salary: int
    from_integration: bool  # has this employee been imported from an integration?


class Model(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    meta: ModelMeta
    sheets: list[Sheet]
    employees: list[Employee] = []  # list of employees

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
