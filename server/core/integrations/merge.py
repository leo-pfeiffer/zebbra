import re
from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from core.dao.integrations import workspace_has_integration
from core.integrations.config import ADAPTERS
from core.logger import logger
from core.schemas.integrations import IntegrationProvider
from core.schemas.models import Employee
from core.schemas.rows import Row, IntegrationValue
from core.schemas.sheets import Sheet
from core.schemas.cache import DataBatch
from core.utils import (
    last_of_same_month,
    first_of_same_month,
    number_of_overlapping_days,
    share_of_period,
)


async def merge_accounting_integration_data(
    sheet: Sheet, workspace_id: str, from_date: date
):
    """
    Adds the integration values to a sheet inplace.
    :param sheet:
    :param workspace_id:
    :param from_date:
    :return:
    """

    data_batches: dict[IntegrationProvider, DataBatch] = {}

    for integration in ADAPTERS.keys():
        adapter = ADAPTERS[integration](workspace_id)
        if adapter.api_type() == "accounting":
            data_batches[integration] = await adapter.get_data(from_date)

    # assumptions
    for row in sheet.assumptions:
        process_row(row, data_batches)

    # sections
    for section in sheet.sections:
        for row in section.rows:
            process_row(row, data_batches=data_batches)
        process_row(section.end_row, data_batches)

    return sheet


async def merge_payroll_integration_data(
    employees: list[Employee], workspace_id: str, from_date: date
):
    """
    Adds the integration values to a list of employees in place
    :param employees:
    :param workspace_id:
    :param from_date:
    :return:
    """
    for integration in ADAPTERS.keys():
        adapter = ADAPTERS[integration](workspace_id)
        if adapter.api_type() == "payroll" and await workspace_has_integration(
            workspace_id, adapter.integration()
        ):
            employees_from_adapter = await adapter.get_data(from_date)
            employees.extend(employees_from_adapter)

    return employees


def aggregate_payroll_info(
    employees: list[Employee], from_date: date, to_date: date = date.today()
):
    months = months_list_from_date(from_date, to_date)
    months_salary_map = total_salary_per_month(months, employees)
    values = []
    for m in months:
        values.append(IntegrationValue(date=m, value=months_salary_map[m]))
    return values


def total_salary_per_month(months: list[date], employees: list[Employee]):
    month_salary_map = {m: 0 for m in months}
    for eom in months:
        som = first_of_same_month(eom)
        for e in employees:
            if e.end_date is None:
                end_point = eom + relativedelta(months=1)
            else:
                end_point = e.end_date.to_date()
            overlap = number_of_overlapping_days(
                (som, eom), (e.start_date.to_date(), end_point)
            )
            if overlap > 0:
                share = share_of_period(overlap, (som, eom))
                month_salary_map[eom] += share * e.monthly_salary
    return month_salary_map


def months_list_from_date(from_date: date, to_date: date = date.today()) -> list[date]:
    from_date = last_of_same_month(from_date)
    to_date = last_of_same_month(to_date)

    months = []
    date_it = from_date
    while date_it <= to_date:
        months.append(date_it)
        date_it = last_of_same_month(date_it + relativedelta(months=1))

    return months


def parse_value(value_string: str) -> tuple[IntegrationProvider, str]:
    """
    Values are of format Integration[End Point]
    :param value_string: string containing the value
    :return: parsed value string
    """
    # ignore warning
    if not re.compile(r"[a-zA-Z]+\[[a-zA-Z\s\d]+\]").fullmatch(value_string):  # noqa
        raise ValueError(f"Invalid value string {value_string}")
    try:
        segments: list[str | IntegrationProvider] = value_string.split("[")
        assert len(segments) == 2
        assert segments[1].endswith("]")
        integration: IntegrationProvider = segments[0]
        endpoint: str = segments[1][:-1]
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
    integration, endpoint = parse_value(row.integration_name)

    # integration must be supported
    if (
        integration not in data_batches
        or endpoint not in data_batches[integration].data
    ):
        logger.error(
            f"Unification mismatch: Integration {integration}, endpoint {endpoint}"
        )
        integration_values = None

    # this is the standard case
    else:
        # use sorted dates to retrieve the IntegrationValues
        integration_values = [
            IntegrationValue(
                date=datetime.strptime(timestamp, "%Y-%m-%d").date(),
                value=data_batches[integration].data[endpoint][timestamp],
            )
            for timestamp in data_batches[integration].dates
        ]

    row.integration_values = integration_values

    return row
