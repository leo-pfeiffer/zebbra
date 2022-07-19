import asyncio
from datetime import date, datetime, timezone

from dateutil.relativedelta import relativedelta

from core.dao.integrations import workspace_has_integration
from core.integrations.adapters.adapter import FetchAdapter
from core.integrations.oauth.xero_oauth import (
    xero_integration_oauth,
    API_URL_SUFFIX,
)
from core.schemas.cache import DataBatch
from core.schemas.integrations import IntegrationProvider
from core.utils import last_of_same_month


class XeroFetchAdapter(FetchAdapter):

    _integration: IntegrationProvider = "Xero"
    _api_type = "accounting"

    def __init__(self, workspace_id: str):
        self._workspace_id = workspace_id

    @property
    def workspace_id(self):
        return self._workspace_id

    @classmethod
    def integration(cls):
        return cls._integration

    @classmethod
    def api_type(cls):
        return cls._api_type

    async def get_data(self, from_date: date) -> DataBatch:
        """
        Retrieve and process the P&L and balance sheet data from XERO
        :param from_date: date from which onwards to get the data
        :return: P&L and balance sheet data
        """

        # return empty batch if Xero not configured for workspace
        if not await workspace_has_integration(self.workspace_id, self.integration()):
            return DataBatch(dates=[], data={})

        # check if we can use cache
        cache_date = self._cache_date(from_date)
        if cached := await self.get_cached(cache_date):
            return cached

        # if no cache, retrieve from Xero API
        batches = await self._get_batches(from_date)

        processed = [self._process_batch(batch) for batch in batches]
        merged = self._merge_batches(processed)

        data_batch = DataBatch(**merged)

        # cache result
        await self.set_cached(data_batch, cache_date)

        return data_batch

    async def get_data_endpoints(self, from_date: date) -> list[str]:
        """
        Retrieve all data points that are available for XERO from a certain date onwards
        :param from_date: date from which onwards to find the endpoints
        :return: list of endpoints
        """

        # return empty list if Xero not configured for workspace
        if not await workspace_has_integration(self.workspace_id, self.integration()):
            return []

        # check if we can use cache of batch data
        actual_from_date = int(
            datetime.combine(
                last_of_same_month(self._get_last_month_with_31_days(from_date)),
                datetime.min.time(),
            ).timestamp()
        )
        if cached := await self.get_cached(actual_from_date):
            return sorted(list(cached.data.keys()))

        # no cache available -> retrieve from Xero API and process
        batches = await self._get_batches(from_date)

        data_points = set()

        for batch in batches:
            assert batch["Status"] == "OK"
            assert len(batch["Reports"]) == 1
            report = batch["Reports"][0]
            assert report["Rows"][0]["RowType"] == "Header"

            for row in report["Rows"][1:]:
                for sub_row in row["Rows"]:
                    assert sub_row["RowType"] in ["Row", "SummaryRow"]
                    data_points.add(sub_row["Cells"][0]["Value"])

        return sorted(list(data_points))

    async def _get_batches(self, from_date: date):
        """
        Retrieve the batches from the Xero API
        :param from_date: Date from which on to get the batches
        :return: batches
        """
        batch_periods = self._create_batch_periods(from_date, date.today())

        pl_batches = await asyncio.gather(
            *[self._retrieve_profit_and_loss(p[0], p[1]) for p in batch_periods]
        )

        bs_batches = await asyncio.gather(
            *[self._retrieve_balance_sheet(p[1]) for p in batch_periods]
        )

        return pl_batches + bs_batches

    def _process_batch(self, batch):
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
            self._date_from_string(cell["Value"], ["%d %b %y", "%d %b %Y"])
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

    def _create_batch_periods(self, from_date: date, to_date: date):
        """
        Create the date periods for fetching the Xero data in multiple batches
        :param from_date: Date in first month to get
        :param to_date: Date in last month to get
        :return: List containing time periods to get in individual batches
        """
        periods: list[tuple[date, date]] = []
        period_start = from_date
        while period_start < to_date:

            period_start = last_of_same_month(
                self._get_last_month_with_31_days(period_start)
            )

            # covers one year
            period_end = last_of_same_month(period_start + relativedelta(months=11))

            if period_end >= to_date:
                period_end = last_of_same_month(to_date)

            periods.append((period_start, period_end))
            period_start = period_end + relativedelta(months=1)

        return periods

    async def _retrieve_profit_and_loss(self, from_date: date, to_date: date):
        """
        Retrieve the P&L data from the XERO API between two dates. The dates must be within
        365 days of each other
        :param from_date: date from which onwards to get the data
        :param to_date: date until which to get data
        :return:
        """

        # must be within 365 days of each other
        assert from_date + relativedelta(years=1) > to_date

        integration_access = await xero_integration_oauth.get_integration_access(
            self.workspace_id
        )

        resp = await xero_integration_oauth.oauth_app.get(
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

    async def _retrieve_balance_sheet(self, to_date: date):
        """
        Retrieve the P&L data from the XERO API between two dates. The dates must be within
        365 days of each other
        :param to_date: date until which to get data
        :return:
        """

        integration_access = await xero_integration_oauth.get_integration_access(
            self.workspace_id
        )

        resp = await xero_integration_oauth.oauth_app.get(
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
