from datetime import date

from core.dao.integrations import workspace_has_integration
from core.integrations.adapters.adapter import FetchAdapter
from core.integrations.oauth.gusto_oauth import gusto_integration_oauth
from core.logger import logger
from core.schemas.integrations import IntegrationProvider
from core.schemas.models import Employee
from core.schemas.utils import DateString


class GustoFetchAdapter(FetchAdapter):

    _integration: IntegrationProvider = "Gusto"
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

        # return empty list if gusto is not configured for the workspace
        if not await workspace_has_integration(self.workspace_id, self.integration()):
            return []

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

        resp.raise_for_status()
        return resp.json()

    def _process_employees(self, employees, from_date: date) -> list[Employee]:
        processed = []

        # Convert each raw employee object into an `Employee` object
        for raw_employee in employees:

            # if employee has no jobs, skip it
            if len(raw_employee["jobs"]) == 0:
                logger.error("No current job found")
                continue

            # get the job objects from the raw employee that the raw employee
            #  held least and most recently
            least_recent_job, most_recent_job = self._get_relevant_jobs(raw_employee)

            # terminated: has the employee been terminated
            # last_termination_date: last date the employee has been terminated
            terminated, last_termination_date = self._get_termination_info(raw_employee)

            # skip terminated employees without termination date
            if terminated and last_termination_date is None:
                logger.error("Terminated, but no terminations")
                continue

            # do not consider employees who were terminated before the start date
            if last_termination_date is not None and last_termination_date < from_date:
                continue

            # calculate the monthly salary of the employee based on the most recent job
            monthly_salary = self._get_monthly_salary(raw_employee, most_recent_job)

            # skip if no salary found
            if monthly_salary is None:
                continue

            # get the department, if available
            department = (
                "" if raw_employee["department"] is None else raw_employee["department"]
            )

            if last_termination_date is not None:
                last_termination_date = DateString(last_termination_date)

            # Create the `Employee` instance
            employee = Employee(
                name=raw_employee["first_name"] + " " + raw_employee["last_name"],
                start_date=DateString(least_recent_job["hire_date"]),
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
        Extract the most recent and least recent jobs from an employee
        :return: (least recent job, most recent job)
        """
        least_recent_job = None
        most_recent_job = None

        # iterate over all jobs the employee has had
        for job in raw_employee["jobs"]:

            # convert hire date string to date
            job["hire_date"] = self._date_from_string(job["hire_date"], ["%Y-%m-%d"])

            # check if the current job is more recent than current most recent job
            if (
                most_recent_job is None
                or job["hire_date"] > most_recent_job["hire_date"]
            ):
                most_recent_job = job

            # check if the current job is less recent than current least recent job
            if (
                least_recent_job is None
                or job["hire_date"] < most_recent_job["hire_date"]
            ):
                least_recent_job = job

        return least_recent_job, most_recent_job

    def _get_termination_info(self, raw_employee: dict) -> tuple[bool, date | None]:
        """
        Extract the termination info from an employee
        :return: (terminated true/false, termination date)
        """
        last_termination_date = None

        # check if employee has been terminated
        if terminated := raw_employee["terminated"]:

            # iterate over all terminations that have been noted for the employee
            for termination in raw_employee["terminations"]:

                # convert the effective date string to a date
                termination["effective_date"] = self._date_from_string(
                    termination["effective_date"], ["%Y-%m-%d"]
                )

                # check if the current termination is more recent
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

        # get the compensation that corresponds to the compensation ID of the most
        #  recent job
        for comp in most_recent_job["compensations"]:
            if comp["id"] == most_recent_job["current_compensation_id"]:
                compensation = comp
                break

        # stop if no compensation has been found
        if compensation is None:
            logger.error("Compensation for most recent job not found")
            return None

        # calculate monthly compensation
        unit_rate = float(compensation["rate"])
        payment_unit = compensation["payment_unit"]

        if payment_unit == "Year":
            # convert yearly to monthly salary
            monthly_salary = int(unit_rate / 12)

        elif payment_unit == "Month":
            # monthly salary
            monthly_salary = int(unit_rate)

        elif payment_unit == "Week":
            # convert weekly to monthly salary (approximate)
            monthly_salary = int(unit_rate * 4.33)

        elif payment_unit == "Hour":
            # convert hourly to monthly salary taking into account employment status
            emp_status = raw_employee["current_employment_status"]

            if emp_status == "part_time_twenty_plus_hours":
                # assume 30 hours per week for Part Time 20+ hrs employees
                monthly_salary = int(unit_rate * 30) * 4.33

            elif emp_status == "part_time_under_twenty_hours":
                # assume 20 hours per week for Part Time <20 hrs employees
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
