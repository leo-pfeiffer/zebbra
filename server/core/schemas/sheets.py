import uuid
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

    new_empty_row = dict(
        name="",
        val_type="number",
        editable=True,
        var_type="value",
        time_series=False,
        starting_at=0,
        first_value_diff=False,
        value="0",
        value_1=None,
        integration_values=None,
        decimal_places=0,
    )

    return [
        Sheet(
            meta=SheetMeta(name="Revenues"),
            assumptions=[Row(**new_empty_row)],
            sections=[
                Section(
                    name="", rows=[Row(**new_empty_row)], end_row=Row(**new_empty_row)
                )
            ],
        ),
        Sheet(
            meta=SheetMeta(name="Costs"),
            assumptions=[Row(**new_empty_row)],
            sections=[
                Section(
                    name="Cost of Goods Sold",
                    rows=[Row(**new_empty_row)],
                    end_row=Row(**new_empty_row),
                ),
                Section(
                    name="Operational Costs",
                    rows=[Row(**new_empty_row)],
                    end_row=Row(**new_empty_row),
                ),
                Section(
                    name="Other Costs",
                    rows=[Row(**new_empty_row)],
                    end_row=Row(**new_empty_row),
                ),
            ],
        ),
    ]
