import re
from datetime import date

from core.schemas.integrations import IntegrationProvider
from core.schemas.rows import Row
from core.schemas.sheets import Sheet
from core.schemas.utils import DataBatch
from core.unification.fetch import XeroFetchAdapter


def parse_value(value_string: str) -> tuple[str, str]:
    """
    Values are of format Integration[End Point]
    :param value_string: string containing the value
    :return: parsed value string
    """
    # ignore warning
    if not re.compile(r"[a-zA-Z]+\[[a-zA-Z\s\d]+\]").fullmatch(value_string):  # noqa
        raise ValueError(f"Invalid value string {value_string}")
    try:
        segments = value_string.split("[")
        assert len(segments) == 2
        assert segments[1].endswith("]")
        integration = segments[0]
        endpoint = segments[1][:-1]
        return integration, endpoint
    except AssertionError:
        raise ValueError(f"Invalid value string {value_string}")


def process_row(row: Row, data_batches: dict[IntegrationProvider, DataBatch]) -> Row:
    """
    Inplace modification
    :param row:
    :param data_batches:
    :return:
    """
    if row.var_type != "integration":
        return row

    # catch error here?
    integration, endpoint = parse_value(row.value)
    # todo
    ...
    return row


async def unify_data(sheet: Sheet, workspace_id: str, from_date: date):
    adapter = XeroFetchAdapter(workspace_id)

    data_batches: dict[IntegrationProvider, DataBatch] = {
        "Xero": await adapter.get_data(from_date)
    }

    # assumptions
    for row in sheet.assumptions:
        process_row(row, data_batches)

    # sections
    for section in sheet.sections:
        for row in section.rows:
            process_row(row, data_batches=data_batches)
        process_row(section.end_row, data_batches)

    return Sheet
