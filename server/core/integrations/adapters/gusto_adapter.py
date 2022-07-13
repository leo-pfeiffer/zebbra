from datetime import date

from core.integrations.adapters.adapter import FetchAdapter
from core.schemas.utils import DataBatch

# todo: If we stick with Gusto, this needs to be implemented


class GustoFetchAdapter(FetchAdapter):

    _integration = "Gusto"

    def __init__(self, workspace_id: str):
        self._workspace_id = workspace_id

    @property
    def workspace_id(self):
        return self._workspace_id

    @classmethod
    def integration(cls):
        return cls._integration

    async def get_data(self, from_date: date) -> DataBatch:
        """
        This is the main method called during the merging procedure to add the
        integration data to the models.
        The method must be overridden by child classes and should implement the
        process to retrieve the data from the integration API or a cache.
        The data must be converted into a DataBatch object.
        Caching should be implemented as far as possible
        :param from_date: date from which onwards to get the data
        :return: DataBatch containing the data from the integration
        """
        # todo
        ...

    async def get_data_endpoints(self, from_date: date) -> list[str]:
        """
        This method should return a list of available data endpoints for the
        integration. It must be overridden by the child class and usually
        makes a call to the integration API to retrieve the available endpoints.
        Caching should be implemented as far as possible
        :param from_date: date from which onwards to get the data
        :return: List of available data endpoints for the integration
        """
        # todo
        ...
