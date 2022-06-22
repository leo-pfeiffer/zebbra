from enum import Enum


class VarType(Enum):
    manual = "manual"
    integration = "integration"
    relation = "relation"


class ValType(Enum):
    number: "number"
    currency: "currency"
    percentage: "percentage"


class RowRef:
    """
    Reference object for expressions.
    Examples:
        - RowRef("row1") references the value in the same column,
            in the row with ID "row1"
        - RowRef("row1", 1) references row the value in the next column,
            in the row with ID "row1"
        - RowRef("row1", -1) references row the value in the previous column,
            in the row with ID "row1"
    """
    row_id: str
    offset: int
