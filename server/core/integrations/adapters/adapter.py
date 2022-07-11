from abc import ABC, abstractmethod
from calendar import monthrange
from datetime import date, datetime, timezone

from dateutil.relativedelta import relativedelta

from core.dao.integrations import get_integration_cache, set_integration_cache
from core.schemas.integrations import IntegrationProvider
from core.schemas.utils import DataBatch, DataBatchCache


class FetchAdapter(ABC):

    _integration: IntegrationProvider

    @abstractmethod
    def __init__(self, workspace_id: str):
        self._workspace_id = workspace_id

    @property
    @abstractmethod
    def workspace_id(self):
        raise NotImplementedError("Abstract method must be implemented by child class.")

    @classmethod
    @abstractmethod
    def integration(cls):
        return cls._integration

    @abstractmethod
    async def get_data(self, from_date: date) -> DataBatch:
        raise NotImplementedError("Abstract method must be implemented by child class.")

    @abstractmethod
    async def get_data_endpoints(self, from_date: date) -> list[str]:
        raise NotImplementedError("Abstract method must be implemented by child class.")

    @staticmethod
    def _date_from_string(date_string):
        try:
            return datetime.strptime(date_string, "%d %b %y").date()
        except ValueError:
            return datetime.strptime(date_string, "%d %b %Y").date()

    @staticmethod
    def _get_last_month_with_31_days(the_date: date) -> date:
        """
        Return the last date in the last month before a date that had 31 days
        :param the_date: original date
        :return: new date
        """
        while monthrange(the_date.year, the_date.month)[1] != 31:
            the_date -= relativedelta(months=1)
        return the_date

    @staticmethod
    def _last_of_same_month(the_date: date) -> date:
        """
        Return the last date of the month
        :param the_date: date for whose month to retrieve the last date
        :return: date
        """
        day = monthrange(the_date.year, the_date.month)[1]
        return date(the_date.year, the_date.month, day)

    async def get_cached(self, from_date: int) -> DataBatch | None:
        cached = await get_integration_cache(
            self.workspace_id, self.integration(), from_date
        )
        if cached:
            return cached.to_data_batch()

    async def set_cached(self, data_batch: DataBatch, from_date: int):

        cache_obj = DataBatchCache(
            data=data_batch.data,
            dates=data_batch.dates,
            created_at=datetime.now().astimezone(timezone.utc),
            workspace_id=self.workspace_id,
            integration=self.integration,
            from_date=from_date,
        )
        return await set_integration_cache(cache_obj)

    @staticmethod
    def _merge_batches(batches: list):
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
                    timeseries[timestamp] = None

        dates = sorted(list(timestamp_set))

        return {"dates": dates, "data": data}
