import uuid
from typing import Literal

from datetime import date
from bson import ObjectId
from pydantic import BaseModel, Field

from core.schemas.rows import DateValue, Row
from core.schemas.utils import PyObjectId, DateString
from core.schemas.sheets import Sheet, Section


class Employee(BaseModel):
    id: str = Field(default_factory=lambda: str(int(uuid.uuid4())), alias="_id")
    name: str | None
    start_date: DateString
    end_date: DateString | None
    title: str | None
    department: str | None
    monthly_salary: int
    from_integration: bool  # has this employee been imported from an integration?


class UpdateEmployee(BaseModel):
    name: str | None
    start_date: DateString
    end_date: DateString | None
    title: str | None
    department: str | None
    monthly_salary: int
    from_integration: bool  # has this employee been imported from an integration?


class Payroll(BaseModel):
    payroll_values: list[DateValue]  # calculated on the fly from employees
    employees: list[Employee]


class ModelMeta(BaseModel):
    name: str
    admins: list[PyObjectId]  # list of user_ids
    editors: list[PyObjectId]  # list of user_ids
    viewers: list[PyObjectId]  # list of user_ids
    workspace: PyObjectId  # workspace id
    starting_month: date
    starting_balance: float = 0

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Model(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    meta: ModelMeta
    sheets: list[Sheet]
    # employees: list[Employee] = []  # list of employees
    payroll: Payroll

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateModel(BaseModel):
    meta: ModelMeta
    sheets: list[Sheet]
    payroll: Payroll

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


def create_new_demo_model(
        admin_id: str | PyObjectId,
        workspace_id: str | PyObjectId,
        model_template: Model
) -> Model:
    new_meta = model_template.meta
    new_meta.admins = [admin_id]
    new_meta.editors = []
    new_meta.viewers = []
    new_meta.workspace = workspace_id

    return Model(
        meta=new_meta,
        sheets=model_template.sheets,
        payroll=model_template.payroll
    )
