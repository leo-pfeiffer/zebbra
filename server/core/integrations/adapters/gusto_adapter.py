from datetime import date

from core.integrations.adapters.adapter import FetchAdapter
from core.integrations.oauth.gusto_oauth import gusto_integration_oauth
from core.logger import logger
from core.schemas.models import Employee


class GustoFetchAdapter(FetchAdapter):

    _integration = "Gusto"
    _api_type = "payroll"

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

    async def get_data(self, from_date: date) -> list[Employee]:
        """
        This is the main method called during the merging procedure to add the
        integration data to the models.
        The method must be overridden by child classes and should implement the
        process to retrieve the data from the integration API or a cache.
        The data must be converted into a list of Employee objects.
        Caching should be implemented as far as possible
        :param from_date: date from which onwards to get the data
        :return: DataBatch containing the data from the integration
        """

        # check if we can use cache
        cache_date = self._cache_date(from_date)
        if cached := await self.get_cached(cache_date):
            return cached

        # if no cache, retrieve from Xero API
        employees = await self._get_employees()

        processed = self._process_employees(employees, from_date)

        await self.set_cached(processed, cache_date)

        return processed

    async def _get_employees(self):

        integration_access = await gusto_integration_oauth.get_integration_access(
            self.workspace_id
        )

        resp = await gusto_integration_oauth.oauth_app.get(
            f"v1/companies/{integration_access.tenant_id}/employees",
            token=integration_access.token.dict(),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        # todo try "include" param

        resp.raise_for_status()
        return resp.json()

    def _process_employees(self, employees, from_date: date) -> list[Employee]:
        processed = []
        for raw_employee in employees:

            # find current job
            if len(raw_employee["jobs"]) == 0:
                logger.error("No current job found")
                continue

            least_recent_job, most_recent_job = self._get_relevant_jobs(raw_employee)

            # get termination
            terminated, last_termination_date = self._get_termination_info(raw_employee)

            if terminated and last_termination_date is None:
                logger.error("Terminated, but no terminations")
                continue

            # skip employees who were terminated before start date
            if last_termination_date is not None and last_termination_date < from_date:
                continue

            monthly_salary = self._get_monthly_salary(raw_employee, most_recent_job)

            if monthly_salary is None:
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

    def _get_relevant_jobs(self, raw_employee: dict) -> tuple[dict, dict]:
        """
        Extract the most recent and least recent jobs from an employee.
        :return (least recent job, most recent job)
        """
        least_recent_job = None
        most_recent_job = None
        for job in raw_employee["jobs"]:

            job["hire_date"] = self._date_from_string(job["hire_date"], ["%Y-%m-%d"])

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
        return least_recent_job, most_recent_job

    def _get_termination_info(self, raw_employee: dict) -> tuple[bool, date | None]:
        """
        Extract the termination info from an employee.
        :return: (terminated true/false, termination date)
        """
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
        return terminated, last_termination_date

    @staticmethod
    def _get_monthly_salary(raw_employee: dict, most_recent_job: dict) -> int | None:
        """
        Extract the monthly salary from an employee
        :param raw_employee: Raw employee dict
        :param most_recent_job: Most recent job object
        :return: monthly salary, None if none found
        """
        # get compensation
        compensation = None
        for comp in most_recent_job["compensations"]:
            if comp["id"] == most_recent_job["current_compensation_id"]:
                compensation = comp
                break
        if compensation is None:
            logger.error("Compensation for most recent job not found")
            return None

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
                monthly_salary = int(unit_rate * 30) * 4.33
            elif emp_status == "part_time_under_twenty_hours":
                monthly_salary = int(unit_rate * 20) * 4.33
            else:
                # count all else as full time
                monthly_salary = int(unit_rate * 40) * 4.33
        else:
            logger.error(f"Cannot process payment unit {payment_unit}")
            return None

        return monthly_salary

    async def get_data_endpoints(self, from_date: date) -> list[str]:
        raise NotImplementedError("Payroll API type does not support endpoints.")
