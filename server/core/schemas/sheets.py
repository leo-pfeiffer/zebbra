from typing import Literal

from bson import ObjectId
from pydantic import BaseModel
from core.schemas.rows import Row


class SheetMeta(BaseModel):
    name: Literal["Revenues", "Costs"]


class Section(BaseModel):
    name: str
    rows: list[Row]
    end_row: Row | None


class Sheet(BaseModel):
    meta: SheetMeta
    assumptions: list[Row]
    sections: list[Section]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


def create_default_sheets():
    return [
        Sheet(meta=SheetMeta(name="Revenues"), assumptions=[], sections=[]),
        Sheet(meta=SheetMeta(name="Costs"), assumptions=[], sections=[]),
    ]
