import pytest

from core.schemas.utils import DateString


def test_date_string():
    assert DateString.validate("2020-01-01")


def test_date_string_not_a_date():
    with pytest.raises(ValueError):
        DateString.validate("abc")


def test_date_string_wrong_format():
    with pytest.raises(ValueError):
        DateString.validate("01-01-2020")


def test_date_string_leading_zero_year():
    with pytest.raises(ValueError):
        DateString.validate("01-01-0120")


def test_date_string_non_existent_day():
    with pytest.raises(ValueError):
        DateString.validate("2020-02-31")
