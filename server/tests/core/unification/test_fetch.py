from core.unification.fetch import (
    process_batch,
    merge_batches,
    create_batch_periods,
    date_to_string_in_batch,
)
from tests.factory import _read_json
from datetime import date


def test_create_batch_periods():
    periods = create_batch_periods(date(2020, 1, 1), date.today())
    assert True


def test_process_batch():
    batch = _read_json("resources/xero.json")
    x = process_batch(batch)
    assert True


def test_merge_batches():
    batches = _read_json("resources/xero_multi.json")
    batches = [process_batch(b) for b in batches]
    x = merge_batches(batches)
    y = date_to_string_in_batch(x)
    assert True
