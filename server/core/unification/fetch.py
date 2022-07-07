from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import asyncio

from core.unification.xero_oauth import (
    get_xero_integration_access,
    xero,
    API_URL_SUFFIX,
)


def date_from_string(date_string):
    try:
        return datetime.strptime(date_string, "%d %b %y").date()
    except ValueError:
        return datetime.strptime(date_string, "%d %b %Y").date()


def date_to_string_in_batch(batch):
    """
    Convert all dates in a batch into string format YYYY-MM-DD
    :param batch: The batch to process
    :return: Converted batch
    """

    data = {}

    for title, timeseries in batch["data"].items():
        data[title] = {}
        for timestamp, value in timeseries.items():
            string_date = timestamp.strftime("%Y-%m-%d")
            data[title][string_date] = value

    dates = [d.strftime("%Y-%m-%d") for d in batch["dates"]]

    return {"dates": dates, "data": data}


def merge_batches(batches: list):
    """
    Merge a list of batches
    :param batches: a list of batches retrieved from the XERO api
    :return: A single batch merged from all batches
    """
    if len(batches) == 0:
        return {}
    if len(batches) == 1:
        return batches[0]

    timestamp_set = set(batches[0]["dates"])
    data = {**batches[0]["data"]}

    for batch in batches[1:]:
        for title, timeseries in batch["data"].items():
            for timestamp in timeseries.keys():
                if title not in data:
                    data[title] = {}
                data[title][timestamp] = timeseries[timestamp]
                timestamp_set.add(timestamp)

    # fill gaps with 0
    for timestamp in list(timestamp_set):
        for _, timeseries in data.items():
            if timestamp not in timeseries:
                timeseries[timestamp] = 0  # todo check if this should be NaN etc.

    dates = sorted(list(timestamp_set))

    return {"dates": dates, "data": data}


def process_batch(batch):
    """
    Convert a raw batch response from the XERO api into a normalized schema.
    :param batch: unprocessed batch
    :return: processed batch
    """

    # preliminary checks
    assert batch["Status"] == "OK"
    assert len(batch["Reports"]) == 1

    report = batch["Reports"][0]

    # get the dates
    assert report["Rows"][0]["RowType"] == "Header"
    dates = [
        date_from_string(cell["Value"])
        for cell in report["Rows"][0]["Cells"]
        if cell["Value"] != ""
    ]

    data = {}
    for row in report["Rows"][1:]:
        assert row["RowType"] == "Section"
        for sub_row in row["Rows"]:

            assert sub_row["RowType"] in ["Row", "SummaryRow"]
            cells = sub_row["Cells"]
            title = cells[0]["Value"]

            value_cells = cells[1:]
            assert len(dates) == len(value_cells)
            values = {}
            for i in range(len(value_cells)):
                values[dates[i]] = float(value_cells[i]["Value"])

            assert title not in data
            data[title] = values

    return {"dates": dates, "data": data}


def get_last_month_with_31_days(the_date: date) -> date:
    """
    Return the last date in the last month before a date that had 31 days
    :param the_date: original date
    :return: new date
    """
    while monthrange(the_date.year, the_date.month)[1] != 31:
        the_date -= relativedelta(months=1)
    return the_date


def last_of_same_month(the_date: date) -> date:
    """
    Return the last date of the month
    :param the_date: date for whose month to retrieve the last date
    :return: date
    """
    day = monthrange(the_date.year, the_date.month)[1]
    return date(the_date.year, the_date.month, day)


def create_batch_periods(from_date: date, to_date: date):
    """
    Create the date periods for fetching the Xero data in multiple batches
    :param from_date: Date in first month to get
    :param to_date: Date in last month to get
    :return: List containing time periods to get in individual batches
    """
    periods: list[tuple[date, date]] = []
    period_start = from_date
    while period_start < to_date:

        period_start = last_of_same_month(get_last_month_with_31_days(period_start))

        # covers one year
        period_end = last_of_same_month(period_start + relativedelta(months=11))

        if period_end >= to_date:
            period_end = last_of_same_month(to_date)

        periods.append((period_start, period_end))
        period_start = period_end + relativedelta(months=1)

    return periods


# todo from_date should be retrieved from model
async def get_xero_data_from_data(workspace_id: str, from_date: date):
    """
    Retrieve and process the P&L and balance sheet data from XERO
    :param workspace_id: ID of the workspace
    :param from_date: date from which onwards to get the data
    :return: P&L and balance sheet data
    """
    pl_batches = await retrieve_profit_and_loss_from_date(workspace_id, from_date)
    bs_batches = await retrieve_balance_sheet_from_date(workspace_id, from_date)
    processed = [process_batch(batch) for batch in pl_batches + bs_batches]
    merged = merge_batches(processed)
    return date_to_string_in_batch(merged)


async def retrieve_profit_and_loss_from_date(workspace_id: str, from_date: date):
    """
    Retrieve the P&L data from the XERO API from a certain date onwards
    :param workspace_id: ID of the workspace
    :param from_date: date from which onwards to get the data
    :return: P&L data
    """
    batch_periods = create_batch_periods(from_date, date.today())

    # asynchronously gather data
    return await asyncio.gather(
        *[retrieve_profit_and_loss(workspace_id, p[0], p[1]) for p in batch_periods]
    )


async def retrieve_balance_sheet_from_date(workspace_id: str, from_date: date):
    """
    Retrieve the balance_sheet data from the XERO API from a certain date onwards
    :param workspace_id: ID of the workspace
    :param from_date: date from which onwards to get the data
    :return: P&L data
    """
    batch_periods = create_batch_periods(from_date, date.today())

    # asynchronously gather data
    return await asyncio.gather(
        *[retrieve_balance_sheet(workspace_id, p[1]) for p in batch_periods]
    )


async def retrieve_profit_and_loss(workspace_id: str, from_date: date, to_date: date):
    """
    Retrieve the P&L data from the XERO API between two dates. The dates must be within
    365 days of each other
    :param workspace_id: ID of the workspace
    :param from_date: date from which onwards to get the data
    :param to_date: date until which to get data
    :return:
    """

    # must be within 365 days of each other
    assert from_date + relativedelta(years=1) > to_date

    integration_access = await get_xero_integration_access(workspace_id)

    resp = await xero.get(
        f"{API_URL_SUFFIX}Reports/ProfitAndLoss",
        token=integration_access.token.dict(),
        params={
            "fromDate": str(from_date),
            "toDate": str(to_date),
            "timeframe": "MONTH",
            "standardLayout": True,
            "periods": 11,
        },
        headers={
            "Xero-Tenant-Id": integration_access.tenant_id,
            "Accept": "application/json",
        },
    )
    resp.raise_for_status()
    return resp.json()


async def retrieve_balance_sheet(workspace_id: str, to_date: date):
    """
    Retrieve the P&L data from the XERO API between two dates. The dates must be within
    365 days of each other
    :param workspace_id: ID of the workspace
    :param to_date: date until which to get data
    :return:
    """

    integration_access = await get_xero_integration_access(workspace_id)

    resp = await xero.get(
        f"{API_URL_SUFFIX}Reports/BalanceSheet",
        token=integration_access.token.dict(),
        params={
            "date": str(to_date),
            "timeframe": "MONTH",
            "standardLayout": True,
            "periods": 11,
        },
        headers={
            "Xero-Tenant-Id": integration_access.tenant_id,
            "Accept": "application/json",
        },
    )
    resp.raise_for_status()
    return resp.json()


# todo from_date should be retrieved from model
async def get_available_data_points(workspace_id: str, from_date: date) -> list[str]:
    """
    Retrieve all data points that are available for XERO from a certain date onwards
    :param workspace_id: ID of the workspace
    :param from_date: date from which onwards to find the endpoints
    :return: list of endpoints
    """
    pl_batches = await retrieve_profit_and_loss_from_date(workspace_id, from_date)
    bs_batches = await retrieve_balance_sheet_from_date(workspace_id, from_date)
    data_points = set()

    for batch in pl_batches + bs_batches:
        assert batch["Status"] == "OK"
        assert len(batch["Reports"]) == 1
        report = batch["Reports"][0]
        assert report["Rows"][0]["RowType"] == "Header"

        for row in report["Rows"][1:]:
            for sub_row in row["Rows"]:
                assert sub_row["RowType"] in ["Row", "SummaryRow"]
                data_points.add(sub_row["Cells"][0]["Value"])

    return sorted(list(data_points))


async def get_transactions(workspace_id: str):

    integration_access = await get_xero_integration_access(workspace_id)

    resp = await xero.get(
        f"{API_URL_SUFFIX}BankTransactions",
        token=integration_access.token.dict(),
        headers={
            "Xero-Tenant-Id": integration_access.tenant_id,
            "Accept": "application/json",
        },
    )
    resp.raise_for_status()
    return resp.json()


async def get_tenants(workspace_id: str):
    integration_access = await get_xero_integration_access(workspace_id)
    token = integration_access.token.dict()

    resp = await xero.get("connections", token=token)
    resp.raise_for_status()
    return resp.json()
