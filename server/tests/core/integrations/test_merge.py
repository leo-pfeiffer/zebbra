from datetime import date

import pytest
from pytest import approx
from pydantic import BaseModel

from core.dao.models import get_revenues_sheet
from core.schemas.integrations import IntegrationProvider
from core.schemas.rows import Row, IntegrationValue
from core.schemas.cache import DataBatch
from core.integrations.merge import (
    parse_value,
    merge_accounting_integration_data,
    process_row,
    months_list_from_date,
    total_salary_per_month,
    aggregate_payroll_info,
)
from core.schemas.utils import DateString
from core.utils import last_of_same_month
from tests.factory import FakeEmployee


def test_parse_value_parses_single_word():
    a, b = parse_value("Xero[Hello]")
    assert a == "Xero"
    assert b == "Hello"


def test_parse_value_parses_two_words():
    a, b = parse_value("Xero[Hello World]")
    assert a == "Xero"
    assert b == "Hello World"


def test_parse_value_missing_endpoint():
    with pytest.raises(ValueError):
        parse_value("Xero[]")


def test_parse_value_missing_integration():
    with pytest.raises(ValueError):
        parse_value("[Hello]")


def test_parse_value_space_in_integration():
    with pytest.raises(ValueError):
        parse_value("Xe ro[Hello]")


@pytest.mark.anyio
async def test_merge_integration_data():
    sheet = await get_revenues_sheet("62b488ba433720870b60ec0a")
    workspace_id = "62bc5706a40e85213c27ce29"
    from_date = date(2020, 1, 1)

    await merge_accounting_integration_data(sheet, workspace_id, from_date)

    assert len(sheet.sections[0].rows[1].integration_values) > 0


def test_process_row_integration():
    row = Row(
        name="name",
        val_type="number",
        editable=True,
        var_type="integration",
        time_series=True,
        starting_at=0,
        first_value_diff=False,
        value="Xero[Total Income]",
        value_1=None,
        integration_values=None,
    )
    data_batches: dict[IntegrationProvider, DataBatch] = {
        "Xero": DataBatch(
            **{
                "dates": ["2020-05-31", "2020-06-30"],
                "data": {"Total Income": {"2020-05-31": "1", "2020-06-30": "2"}},
            }
        )
    }
    process_row(row, data_batches)

    assert row.integration_values == [
        IntegrationValue(date=date(2020, 5, 31), value="1.0"),
        IntegrationValue(date=date(2020, 6, 30), value="2.0"),
    ]


def test_process_row_ignores_formula_row():
    row = Row(
        name="name",
        val_type="number",
        editable=True,
        var_type="formula",
        time_series=True,
        starting_at=0,
        first_value_diff=True,
        value="$-1 * 1.05",
        value_1=100,
        integration_values=None,
    )
    data_batches: dict[IntegrationProvider, DataBatch] = {
        "Xero": DataBatch(
            **{
                "dates": ["2020-05-31", "2020-06-30"],
                "data": {"Total Income": {"2020-05-31": "1", "2020-06-30": "2"}},
            }
        )
    }
    process_row(row, data_batches)

    assert row.integration_values is None


def test_process_row_ignores_value_row():
    row = Row(
        name="name",
        val_type="number",
        editable=True,
        var_type="value",
        time_series=True,
        starting_at=0,
        first_value_diff=False,
        value="500.0",
        value_1=None,
        integration_values=None,
    )
    data_batches: dict[IntegrationProvider, DataBatch] = {
        "Xero": DataBatch(
            **{
                "dates": ["2020-05-31", "2020-06-30"],
                "data": {"Total Income": {"2020-05-31": "1", "2020-06-30": "2"}},
            }
        )
    }
    process_row(row, data_batches)

    assert row.integration_values is None


def test_months_list_from_date():
    months = months_list_from_date(date(2022, 1, 1), date(2022, 4, 1))
    assert len(months) == 4
    assert months == [
        date(2022, 1, 31),
        date(2022, 2, 28),
        date(2022, 3, 31),
        date(2022, 4, 30),
    ]


def test_months_list_from_date_with_last_of_month():
    months = months_list_from_date(date(2022, 1, 31), date(2022, 4, 30))
    assert len(months) == 4
    assert months == [
        date(2022, 1, 31),
        date(2022, 2, 28),
        date(2022, 3, 31),
        date(2022, 4, 30),
    ]


def test_months_list_from_date_same_month():
    months = months_list_from_date(date(2022, 1, 10), date(2022, 1, 31))
    assert len(months) == 1
    assert months == [date(2022, 1, 31)]


def test_months_list_from_date_today():
    months = months_list_from_date(date.today())
    assert len(months) == 1
    assert months == [last_of_same_month(date.today())]


def test_total_salary_per_month():

    employees = [
        FakeEmployee(
            start_date=DateString("2020-01-01"),
            end_date=DateString("2020-03-31"),
            monthly_salary=100,
        ),
        FakeEmployee(
            start_date=DateString("2020-02-01"),
            end_date=DateString("2020-03-31"),
            monthly_salary=100,
        ),
        FakeEmployee(
            start_date=DateString("2020-03-01"),
            end_date=DateString("2020-03-31"),
            monthly_salary=100,
        ),
    ]

    months = months_list_from_date(date(2020, 1, 1), date(2020, 3, 31))

    result = total_salary_per_month(months, employees)  # noqa
    assert result[date(2020, 1, 31)] == 100
    assert result[date(2020, 2, 29)] == 200
    assert result[date(2020, 3, 31)] == 300


def test_total_salary_per_month_mid_month_start():

    employees = [
        FakeEmployee(
            start_date=DateString("2020-01-15"),
            end_date=DateString("2020-03-31"),
            monthly_salary=100,
        ),
    ]

    months = months_list_from_date(date(2020, 1, 1), date(2020, 3, 31))

    result = total_salary_per_month(months, employees)  # noqa
    assert result[date(2020, 1, 31)] == approx(100 * (17 / 31))
    assert result[date(2020, 2, 29)] == 100
    assert result[date(2020, 3, 31)] == 100


def test_total_salary_per_month_mid_month_end():
    employees = [
        FakeEmployee(
            start_date=DateString("2020-01-01"),
            end_date=DateString("2020-03-15"),
            monthly_salary=100,
        ),
    ]

    months = months_list_from_date(date(2020, 1, 1), date(2020, 3, 31))

    result = total_salary_per_month(months, employees)  # noqa
    assert result[date(2020, 1, 31)] == 100
    assert result[date(2020, 2, 29)] == 100
    assert result[date(2020, 3, 31)] == approx(100 * (15 / 31))


def test_total_salary_per_month_sub_month():

    employees = [
        FakeEmployee(
            start_date=DateString("2020-01-15"),
            end_date=DateString("2020-01-20"),
            monthly_salary=100,
        ),
    ]

    months = months_list_from_date(date(2020, 1, 1), date(2020, 3, 31))

    result = total_salary_per_month(months, employees)  # noqa
    assert result[date(2020, 1, 31)] == approx(100 * (6 / 31))
    assert result[date(2020, 2, 29)] == 0
    assert result[date(2020, 3, 31)] == 0


def test_aggregate_payroll_info():

    employees = [
        FakeEmployee(
            start_date=DateString("2020-01-01"),
            end_date=DateString("2020-03-31"),
            monthly_salary=100,
        ),
        FakeEmployee(
            start_date=DateString("2020-02-01"),
            end_date=DateString("2020-03-31"),
            monthly_salary=100,
        ),
        FakeEmployee(
            start_date=DateString("2020-03-01"),
            end_date=DateString("2020-03-31"),
            monthly_salary=100,
        ),
    ]

    result = aggregate_payroll_info(
        employees, date(2020, 1, 1), date(2020, 3, 31)  # noqa
    )

    assert result[0].date == date(2020, 1, 31)
    assert result[1].date == date(2020, 2, 29)
    assert result[2].date == date(2020, 3, 31)

    assert result[0].value == str(float(100))
    assert result[1].value == str(float(200))
    assert result[2].value == str(float(300))
