import uuid
from typing import Literal
from datetime import date
from pydantic import BaseModel, Field


class IntegrationValue(BaseModel):
    date: date
    value: str | None


class Row(BaseModel):
    id: str = Field(
        default_factory=lambda: str(int(uuid.uuid4())), alias="_id"
    )  # required to be able to reference between different variables
    name: str  # e.g. "Churn Rate" -> how is it called?
    val_type: Literal["number", "currency", "percentage"]  # how is it displayed?
    editable: bool  # true, false -> can the user change anything?
    var_type: Literal["value", "formula", "integration"]
    time_series: bool  # is the value changing over time or not?
    starting_at: int  # t + startingAt; default = 0
    first_value_diff: bool  # is the first value different?
    value: str  # parsed in the frontend -> var_type is relevant for this
    value_1: str | None  # only relevant if firstValueDiff == true
    integration_values: list[IntegrationValue] | None
    decimal_places: int = 2
