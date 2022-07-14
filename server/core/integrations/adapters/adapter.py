from abc import ABC, abstractmethod
from calendar import monthrange
from datetime import date, datetime, timezone
from typing import Literal

from dateutil.relativedelta import relativedelta

from core.dao.integrations import get_accounting_cache, set_accounting_cache
from core.schemas.integrations import IntegrationProvider
from core.schemas.models import Employee
from core.schemas.utils import DataBatch, DataBatchCache


class FetchAdapter(ABC):
    """
    Abstract class for fetching data from an integrated app.
    Override this class to implement the integration specific data transformations and
    requests.
    """

    _integration: IntegrationProvider
    _api_type: Literal["accounting", "payroll"]

    @abstractmethod
    def __init__(self, workspace_id: str):
        self._workspace_id = workspace_id

    @property
    @abstractmethod
    def workspace_id(self):
        """
        ID of the workspace for which to fetch data.
        """
        raise NotImplementedError("Abstract method must be implemented by child class.")

    @classmethod
    @abstractmethod
    def integration(cls):
        """
        Name of the integration.
        """
        return cls._integration

    @abstractmethod
    async def get_data(self, from_date: date) -> DataBatch | list[Employee]:
        """
        This is the main method called during the merging procedure to add the
        integration data to the models.
        The method must be overridden by child classes and should implement the
        process to retrieve the data from the integration API or a cache.
        The data must be converted into a DataBatch object (for accounting APIs)
        or a list of employees (for payroll APIs)
        Caching should be implemented as far as possible
        :param from_date: date from which onwards to get the data
        :return: DataBatch containing the data from the integration or list of employees
        """
        raise NotImplementedError("Abstract method must be implemented by child class.")

    @abstractmethod
    async def get_data_endpoints(self, from_date: date) -> list[str]:
        """
        This method should return a list of available data endpoints for the
        integration. It must be overridden by the child class and usually
        makes a call to the integration API to retrieve the available endpoints.
        Caching should be implemented as far as possible
        :param from_date: date from which onwards to get the data
        :return: List of available data endpoints for the integration
        """
        raise NotImplementedError("Abstract method must be implemented by child class.")

    @staticmethod
    def _date_from_string(date_string: str, formats: list[str]) -> date:
        """
        Helper method to convert a date string to datetime date. The method
        checks all formats provided and returns the first match. If none matches, a
        value error is thrown
        :param date_string: Date string
        :param formats: List of formats to check, e.g. ["%d %b %y", "%d %b %Y"]
        :return: datetime.date object
        """
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt).date()
            except ValueError:
                continue

        raise ValueError(f"Date {date_string} could not be matched.")

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

    @staticmethod
    def _cache_date(from_date: date) -> int:
        return int(
            datetime.combine(
                FetchAdapter._last_of_same_month(
                    FetchAdapter._get_last_month_with_31_days(from_date)
                ),
                datetime.min.time(),
            )
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )

    async def get_cached(self, from_date: int) -> DataBatch | list[Employee] | None:
        """
        This method retrieves a cached data batch or employee list for a provided date.
        The method delegates either to the caching method for data batches or to
        employee lists based on the API type
        :param from_date: Date in unix format, converted to UTC for reproducibility
        :return: Data batch if cached, else None
        """
        if self._api_type == "accounting":
            return await self._get_cached_accounting(from_date)
        elif self._api_type == "payroll":
            return await self._get_cached_payroll(from_date)

    async def _get_cached_accounting(self, from_date: int):
        cached = await get_accounting_cache(
            self.workspace_id, self.integration(), from_date
        )
        if cached:
            return cached.to_data_batch()

    async def _get_cached_payroll(self, from_date: int):
        # todo IMPLEMENT!!!
        ...

    async def set_cached(self, data: DataBatch | list[Employee], from_date: int):
        """
        This method caches a data batch for a provided date.
        The method delegates either to the caching method for data batches or to
        employee lists based on the API type
        :param data: Data batch or employee list to cache
        :param from_date: Date in unix format, converted to UTC for reproducibility
        """
        if self._api_type == "accounting":
            return await self._set_cached_accounting(data, from_date)
        elif self._api_type == "payroll":
            return await self._set_cached_payroll(data, from_date)

    async def _set_cached_accounting(self, data_batch: DataBatch, from_date: int):
        cache_obj = DataBatchCache(
            data=data_batch.data,
            dates=data_batch.dates,
            created_at=datetime.now().astimezone(timezone.utc),
            workspace_id=self.workspace_id,
            integration=self.integration(),
            from_date=from_date,
        )
        return await set_accounting_cache(cache_obj)

    async def _set_cached_payroll(self, data_batch: list[Employee], from_date: int):
        # todo IMPLEMENT!!!
        ...

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
