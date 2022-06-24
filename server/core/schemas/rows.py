from typing import Any

from bson import ObjectId
from pydantic import BaseModel

from core.types import RowType, ValType


class RowData(BaseModel):
    """
    Abstract class for row data.
    """

    varType: RowType
    data: Any


class Manual(RowData):
    varType = RowType.manual
    data: dict[str, float]  # column_id: value

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "varType": "manual",
                "data": {
                    "column1": 1.23,
                    "column2": 12.3,
                    "column3": 123,
                },
            }
        }


class Integration(RowData):
    # todo
    varType = RowType.integration
    ...


class Relation(RowData):
    # todo
    varType = RowType.relation
    data: dict[str, float]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "varType": "relation",
                "data": {
                    "expression": "RowRef('row1') + RowRef('row2')",
                    "has_starting_value": True,
                    "starting_value": 123,
                },
            }
        }


class Row(BaseModel):
    name: str
    valType: ValType
    editable: bool
    data: Manual | Integration | Relation

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
