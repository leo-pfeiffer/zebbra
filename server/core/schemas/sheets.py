from bson import ObjectId
from pydantic import BaseModel, Field

from core.models.objects import PyObjectId
from core.schemas.rows import Row


class SheetMeta(BaseModel):
    name: str
    # todo what else?


class SectionModel(BaseModel):
    category: str   # todo: @Patrick, what did we mean by that again?
    rows: list[Row]
    end_row: Row    # todo should we enforce this to be a relation row?


class Section(BaseModel):
    assumptions: list[Row]  # todo should we enforce that Row is a manual row?
    model: SectionModel


class Sheet(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    meta: SheetMeta
    data: list[Section]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

