from datetime import date

import pytest

from core.dao.models import get_revenues_sheet
from core.schemas.integrations import IntegrationProvider
from core.schemas.rows import Row, IntegrationValue
from core.schemas.utils import DataBatch
from core.integrations.merge import parse_value, merge_integration_data, process_row


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

    await merge_integration_data(sheet, workspace_id, from_date)

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
