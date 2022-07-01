from bson import ObjectId
from pydantic import BaseModel
from core.schemas.rows import Row, Relation, Manual


class SheetMeta(BaseModel):
    name: str


class Section(BaseModel):
    name: str
    rows: list[Row]
    end_row: Relation | None


class Sheet(BaseModel):
    meta: SheetMeta
    assumptions: list[Manual]
    sections: list[Section]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
