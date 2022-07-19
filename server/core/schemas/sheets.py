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

    ref1 = str(int(uuid.uuid4()))
    ref2 = str(int(uuid.uuid4()))

    return [
        Sheet(
            meta=SheetMeta(name="Revenues"),
            assumptions=[
                Row(
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
            ],
            sections=[
                Section(
                    name="Product Section 1",
                    rows=[
                        Row(
                            id=ref1,
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
                    ],
                    end_row=Row(
                        name="",
                        val_type="number",
                        editable=True,
                        var_type="formula",
                        time_series=False,
                        starting_at=0,
                        first_value_diff=False,
                        value=f"#{ref1}",
                        value_1=None,
                        integration_values=None,
                        decimal_places=0,
                    ),
                )
            ],
        ),
        Sheet(
            meta=SheetMeta(name="Costs"),
            assumptions=[
                Row(
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
            ],
            sections=[
                Section(
                    name="Product Section 1",
                    rows=[
                        Row(
                            id=ref2,
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
                    ],
                    end_row=Row(
                        name="",
                        val_type="number",
                        editable=True,
                        var_type="formula",
                        time_series=False,
                        starting_at=0,
                        first_value_diff=False,
                        value=f"#{ref2}",
                        value_1=None,
                        integration_values=None,
                        decimal_places=0,
                    ),
                )
            ],
        ),
    ]
