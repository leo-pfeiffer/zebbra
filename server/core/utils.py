from calendar import monthrange
from datetime import date


def last_of_same_month(the_date: date) -> date:
    """
    Return the last date of the month
    :param the_date: date for whose month to retrieve the last date
    :return: date
    """
    day = monthrange(the_date.year, the_date.month)[1]
    return date(the_date.year, the_date.month, day)


def first_of_same_month(the_date: date) -> date:
    """
    Return the first date of the month
    :param the_date: date for whose month to retrieve the first date
    :return: date
    """
    return date(the_date.year, the_date.month, 1)


def number_of_overlapping_days(
    range1: tuple[date, date], range2: tuple[date, date]
) -> int:
    latest_start = max(range1[0], range2[0])
    earliest_end = min(range1[1], range2[1])
    diff = (earliest_end - latest_start).days + 1
    return max(0, diff)


def share_of_period(num_days, date_range: tuple[date, date]):
    total_days = (date_range[1] - date_range[0]).days + 1
    return num_days / total_days
