from datetime import date

from core.integrations.adapters.adapter import FetchAdapter
from core.integrations.oauth.gusto_oauth import gusto_integration_oauth
from core.logger import logger
from core.schemas.models import Employee
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

    async def get_data(self, from_date: date) -> DataBatch | list[Employee]:
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
        # check if we can use cache
        cache_date = self._cache_date(from_date)
        if cached := await self.get_cached(cache_date):
            return cached

        # if no cache, retrieve from Xero API
        employees = await self._get_employees(from_date)

        processed = self._process_employees(employees)

        # todo

    async def _get_employees(self, from_date: date):

        # todo refactor this garbage

        integration_access = await gusto_integration_oauth.get_integration_access(
            self.workspace_id
        )

        resp = await gusto_integration_oauth.oauth_app.get(
            f"v2/companies/{integration_access.tenant_id}/employees",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        # todo try "include" param

        resp.raise_for_status()
        return resp.json()

    def _process_employees(self, employees) -> list[Employee]:
        processed = []
        for raw_employee in employees:

            # find current job
            if len(raw_employee["jobs"]) == 0:
                logger.error("No current job found")
                continue

            least_recent_job = None
            most_recent_job = None
            for job in raw_employee["jobs"]:

                job["hire_date"] = self._date_from_string(
                    job["hire_date"], ["%Y-%m-%d"]
                )

                if (
                    most_recent_job is None
                    or job["hire_date"] > most_recent_job["hire_date"]
                ):
                    most_recent_job = job

                if (
                    least_recent_job is None
                    or job["hire_date"] < most_recent_job["hire_date"]
                ):
                    least_recent_job = job

            # get compensation
            compensation = None
            for comp in most_recent_job["compensations"]:
                if comp["id"] == most_recent_job["current_compensation_id"]:
                    compensation = comp
                    break
            if compensation is None:
                logger.error("Compensation for most recent job not found")

            # calculate monthly compensation
            unit_rate = float(compensation["rate"])
            payment_unit = compensation["payment_unit"]
            if payment_unit == "Year":
                monthly_salary = int(unit_rate / 12)
            elif payment_unit == "Month":
                monthly_salary = int(unit_rate)
            elif payment_unit == "Week":
                monthly_salary = int(unit_rate * 4.33)
            elif payment_unit == "Hour":
                emp_status = raw_employee["current_employment_status"]
                if emp_status == "part_time_twenty_plus_hours":
                    monthly_salary = int(unit_rate * 30)
                elif emp_status == "part_time_under_twenty_hours":
                    monthly_salary = int(unit_rate * 20)
                else:
                    monthly_salary = int(unit_rate * 40)  # count all else as full time
            else:
                logger.error(f"Cannot process payment unit {payment_unit}")
                continue

            # get termination
            last_termination_date = None
            if terminated := raw_employee["terminated"]:
                for termination in raw_employee["terminations"]:
                    termination["effective_date"] = self._date_from_string(
                        termination["effective_date"], ["%Y-%m-%d"]
                    )
                    if (
                        last_termination_date is None
                        or termination["effective_date"] > last_termination_date
                    ):
                        last_termination_date = termination["effective_date"]

            if terminated and last_termination_date is None:
                logger.error("Terminated, but no terminations")
                continue

            department = (
                "" if raw_employee["department"] is None else raw_employee["department"]
            )

            employee = Employee(
                name=raw_employee["first_name"] + " " + raw_employee["last_name"],
                start_date=least_recent_job["hire_date"],
                end_date=last_termination_date,
                title=most_recent_job["title"],
                department=department,
                monthly_salary=monthly_salary,
                from_integration=True,
            )

            processed.append(employee)

        return processed

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
