from datetime import date

from core.utils import share_of_period, number_of_overlapping_days


def test_share_of_period_full_month():
    assert share_of_period(31, (date(2020, 1, 1), date(2020, 1, 31))) == 1


def test_share_of_period_zero():
    assert share_of_period(0, (date(2020, 1, 1), date(2020, 1, 31))) == 0


def test_share_of_period_in_between():
    assert share_of_period(15, (date(2020, 4, 1), date(2020, 4, 30))) == 15 / 30


def test_number_of_overlapping_days_end():
    assert (
        number_of_overlapping_days(
            (date(2020, 1, 1), date(2020, 1, 31)),
            (date(2020, 1, 15), date(2020, 1, 31)),
        )
        == 17
    )


def test_number_of_overlapping_days_start():
    assert (
        number_of_overlapping_days(
            (date(2020, 1, 1), date(2020, 1, 31)),
            (date(2020, 1, 1), date(2020, 1, 15)),
        )
        == 15
    )


def test_number_of_overlapping_days_middle():
    assert (
        number_of_overlapping_days(
            (date(2020, 1, 1), date(2020, 1, 31)),
            (date(2020, 1, 14), date(2020, 1, 15)),
        )
        == 2
    )
