from core.unification.fetch import XeroFetchAdapter
from tests.factory import _read_json
from datetime import date


def test_create_batch_periods():
    # todo
    periods = XeroFetchAdapter("")._create_batch_periods(date(2020, 1, 1), date.today())
    assert True


def test_process_batch():
    # todo
    batch = _read_json("resources/xero_profitloss.json")
    x = XeroFetchAdapter("")._process_batch(batch)
    assert True


def test_process_batch_balance():
    # todo
    batch = _read_json("resources/xero_balance.json")
    x = XeroFetchAdapter("")._process_batch(batch)
    assert True


def test_merge_batches():
    # todo
    xfa = XeroFetchAdapter("")
    batches = _read_json("resources/xero_multi.json")
    batches = [xfa._process_batch(b) for b in batches]
    x = xfa._merge_batches(batches)
    y = xfa._date_to_string_in_batch(x)
    assert True
