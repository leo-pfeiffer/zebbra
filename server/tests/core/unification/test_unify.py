from datetime import date

import pytest

from core.dao.models import get_revenues_sheet
from core.unification.unify import parse_value, unify_data


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
async def test_unify_data():
    sheet = await get_revenues_sheet("62b488ba433720870b60ec0a")
    workspace_id = "62bc5706a40e85213c27ce29"
    from_date = date(2020, 1, 1)

    unified = await unify_data(sheet, workspace_id, from_date)
