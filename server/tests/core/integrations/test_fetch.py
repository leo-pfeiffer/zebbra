from core.schemas.utils import DataBatch
from core.integrations.adapters.xero_adapter import XeroFetchAdapter
from tests.factory import _read_json
from datetime import date


def test_create_batch_periods():
    periods = XeroFetchAdapter("")._create_batch_periods(
        date(2020, 1, 1), date(2022, 7, 8)
    )
    assert len(periods) == 3
    assert periods[0] == (date(2020, 1, 31), date(2020, 12, 31))
    assert periods[1] == (date(2021, 1, 31), date(2021, 12, 31))
    assert periods[2] == (date(2022, 1, 31), date(2022, 7, 31))


def test_create_batch_periods_sub_one_year():
    periods = XeroFetchAdapter("")._create_batch_periods(
        date(2022, 3, 1), date(2022, 7, 8)
    )
    assert len(periods) == 1
    assert periods[0] == (date(2022, 3, 31), date(2022, 7, 31))


def test_create_batch_periods_start_in_short_month():
    periods = XeroFetchAdapter("")._create_batch_periods(
        date(2022, 2, 1), date(2022, 7, 8)
    )
    assert len(periods) == 1
    assert periods[0] == (date(2022, 1, 31), date(2022, 7, 31))


def test_create_batch_periods_end_in_short_month():
    periods = XeroFetchAdapter("")._create_batch_periods(
        date(2022, 3, 1), date(2022, 6, 8)
    )
    assert len(periods) == 1
    assert periods[0] == (date(2022, 3, 31), date(2022, 6, 30))


def test_process_batch():
    batch = _read_json("resources/xero_profitloss.json")
    processed = XeroFetchAdapter("")._process_batch(batch)
    try:
        DataBatch(**processed)
        assert True
    except ValueError:
        assert False


def test_process_batch_balance():
    batch = _read_json("resources/xero_balance.json")
    processed = XeroFetchAdapter("")._process_batch(batch)
    try:
        DataBatch(**processed)
        assert True
    except ValueError:
        assert False


def test_merge_batches():
    xfa = XeroFetchAdapter("")
    batches = _read_json("resources/xero_multi.json")
    batches = [xfa._process_batch(b) for b in batches]
    merged = xfa._merge_batches(batches)
    try:
        DataBatch(**merged)
        assert True
    except ValueError:
        assert False
