from enum import Enum


class RowType(Enum):
    """
    Type of row. Can be one of ['manual', 'integration', 'relation'].
    """
    manual = "manual"
    integration = "integration"
    relation = "relation"


class ValType(Enum):
    """
    Type of value. Can be one of ['number', 'currency', 'percentage']
    """
    number = "number"
    currency = "currency"
    percentage = "percentage"


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
