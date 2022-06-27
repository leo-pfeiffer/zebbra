from bson import ObjectId
from pydantic import BaseModel

from core.types import RowType, ValType


class Row(BaseModel):
    name: str
    valType: ValType
    editable: bool
    varType: RowType
    data: dict  # todo more descriptive type

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Manual(Row):
    varType = RowType.manual
    data: dict[str, float]  # column_id: value

    # "data": {
    #     "column1": 1.23,
    #     "column2": 12.3,
    #     "column3": 123,
    # },


class Integration(Row):
    # todo
    varType = RowType.integration
    data: dict[str, float]


class Relation(Row):
    # todo

    class RelationData(BaseModel):
        expression: str
        has_starting_value: bool
        starting_value: float

        class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True
            schema_extra = {
                "example": {
                    "expression": "RowRef('row1') + RowRef('row2')",
                    "has_starting_value": True,
                    "starting_value": 123,
                }
            }

    varType = RowType.relation
    data: RelationData
