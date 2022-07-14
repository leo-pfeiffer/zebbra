from core.integrations.adapters.gusto_adapter import GustoFetchAdapter
from core.schemas.cache import DataBatch
from core.integrations.adapters.xero_adapter import XeroFetchAdapter
from tests.factory import _read_json
from datetime import date
from copy import deepcopy


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


def test_gusto_process_employees():
    batch = _read_json("resources/gusto_employees.json")
    processed = GustoFetchAdapter("")._process_employees(batch, date(2020, 1, 1))
    assert True
    # todo add actual test


def test_gusto_process_employees_handle_termination():

    base = dict(
        last_name="Doe",
        jobs=[
            dict(
                title="Officer",
                current_compensation_id=1,
                hire_date="2020-01-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Month",
                        rate="5000",
                        effective_date="2020-01-01",
                    )
                ],
            ),
        ],
        department="Government",
        terminated=True,
        current_employment_status="full-time",
    )

    terminated1 = deepcopy(base)
    terminated2 = deepcopy(base)

    terminated1["first_name"] = "1"
    terminated2["first_name"] = "2"

    terminated1["terminations"] = [dict(effective_date="2020-01-01")]
    terminated2["terminations"] = [dict(effective_date="2020-06-01")]

    batch = [terminated1, terminated2]

    processed = GustoFetchAdapter("")._process_employees(batch, date(2020, 3, 1))

    assert len(processed) == 1
    assert processed[0].name == "2 Doe"


def test_gusto_process_employees_correct_end_date():

    base = dict(
        first_name="John",
        last_name="Doe",
        jobs=[
            dict(
                title="Officer",
                current_compensation_id=1,
                hire_date="2020-01-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Month",
                        rate="5000",
                        effective_date="2020-01-01",
                    )
                ],
            ),
            dict(
                title="Officer 2",
                current_compensation_id=1,
                hire_date="2020-02-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Month",
                        rate="6000",
                        effective_date="2020-02-01",
                    )
                ],
            ),
        ],
        department="Government",
        terminated=True,
        current_employment_status="full-time",
        terminations=[
            dict(effective_date="2020-01-01"),
            dict(effective_date="2020-02-01"),
            dict(effective_date="2020-03-01"),
        ],
    )

    processed = GustoFetchAdapter("")._process_employees([base], date(2020, 3, 1))

    assert len(processed) == 1
    assert processed[0].end_date == date(2020, 3, 1)


def test_gusto_process_employees_correct_start_date():

    base = dict(
        first_name="John",
        last_name="Doe",
        jobs=[
            dict(
                title="Officer 2",
                current_compensation_id=1,
                hire_date="2020-02-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Month",
                        rate="6000",
                        effective_date="2020-02-01",
                    )
                ],
            ),
            dict(
                title="Officer",
                current_compensation_id=1,
                hire_date="2020-01-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Month",
                        rate="5000",
                        effective_date="2020-01-01",
                    )
                ],
            ),
        ],
        department="Government",
        terminated=False,
        current_employment_status="full-time",
        terminations=[],
    )

    processed = GustoFetchAdapter("")._process_employees([base], date(2020, 3, 1))

    assert len(processed) == 1
    assert processed[0].start_date == date(2020, 1, 1)


def test_gusto_process_employees_handle_compensation_monthly():
    base = dict(
        first_name="John",
        last_name="Doe",
        jobs=[
            dict(
                title="Officer",
                current_compensation_id=1,
                hire_date="2020-01-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Month",
                        rate="5000",
                        effective_date="2020-01-01",
                    )
                ],
            ),
        ],
        department="Government",
        terminated=False,
        current_employment_status="full-time",
        terminations=[],
    )

    batch = [base]

    processed = GustoFetchAdapter("")._process_employees(batch, date(2020, 3, 1))

    assert len(processed) == 1
    assert processed[0].monthly_salary == 5000


def test_gusto_process_employees_handle_compensation_yearly():
    base = dict(
        first_name="John",
        last_name="Doe",
        jobs=[
            dict(
                title="Officer",
                current_compensation_id=1,
                hire_date="2020-01-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Year",
                        rate="60000",
                        effective_date="2020-01-01",
                    )
                ],
            ),
        ],
        department="Government",
        terminated=False,
        current_employment_status="full-time",
        terminations=[],
    )

    batch = [base]

    processed = GustoFetchAdapter("")._process_employees(batch, date(2020, 3, 1))

    assert len(processed) == 1
    assert processed[0].monthly_salary == 5000


def test_gusto_process_employees_handle_compensation_weekly():
    base = dict(
        first_name="John",
        last_name="Doe",
        jobs=[
            dict(
                title="Officer",
                current_compensation_id=1,
                hire_date="2020-01-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Week",
                        rate="1000",
                        effective_date="2020-01-01",
                    )
                ],
            ),
        ],
        department="Government",
        terminated=False,
        current_employment_status="full-time",
        terminations=[],
    )

    batch = [base]

    processed = GustoFetchAdapter("")._process_employees(batch, date(2020, 3, 1))

    assert len(processed) == 1
    assert processed[0].monthly_salary == 4330


def test_gusto_process_employees_handle_compensation_hourly_full_time():
    base = dict(
        first_name="John",
        last_name="Doe",
        jobs=[
            dict(
                title="Officer",
                current_compensation_id=1,
                hire_date="2020-01-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Hour",
                        rate="10",
                        effective_date="2020-01-01",
                    )
                ],
            ),
        ],
        department="Government",
        terminated=False,
        current_employment_status="full-time",
        terminations=[],
    )

    batch = [base]

    processed = GustoFetchAdapter("")._process_employees(batch, date(2020, 3, 1))

    assert len(processed) == 1
    assert processed[0].monthly_salary == 10 * 40 * 4.33


def test_gusto_process_employees_handle_compensation_hourly_part_time_twenty_plus():
    base = dict(
        first_name="John",
        last_name="Doe",
        jobs=[
            dict(
                title="Officer",
                current_compensation_id=1,
                hire_date="2020-01-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Hour",
                        rate="10",
                        effective_date="2020-01-01",
                    )
                ],
            ),
        ],
        department="Government",
        terminated=False,
        current_employment_status="part_time_twenty_plus_hours",
        terminations=[],
    )

    batch = [base]

    processed = GustoFetchAdapter("")._process_employees(batch, date(2020, 3, 1))

    assert len(processed) == 1
    assert processed[0].monthly_salary == 10 * 30 * 4.33


def test_gusto_process_employees_handle_compensation_hourly_part_time_under_twenty():
    base = dict(
        first_name="John",
        last_name="Doe",
        jobs=[
            dict(
                title="Officer",
                current_compensation_id=1,
                hire_date="2020-01-01",
                compensations=[
                    dict(
                        id=1,
                        payment_unit="Hour",
                        rate="10",
                        effective_date="2020-01-01",
                    )
                ],
            ),
        ],
        department="Government",
        terminated=False,
        current_employment_status="part_time_under_twenty_hours",
        terminations=[],
    )

    batch = [base]

    processed = GustoFetchAdapter("")._process_employees(batch, date(2020, 3, 1))

    assert len(processed) == 1
    assert processed[0].monthly_salary == 10 * 20 * 4.33
