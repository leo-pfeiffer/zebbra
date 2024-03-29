from locust import HttpUser, task, between
from mixins import JohnDoeMixin


class LocustModels(JohnDoeMixin, HttpUser):
    wait_time = between(1, 5)
    weight = 10

    model_id = "62b488ba433720870b60ec0a"

    @task
    def model_meta(self):
        self.client.get(
            "/model/meta",
            params={"model_id": self.model_id},
            name="/model/meta",
        )

    @task
    def model_users(self):
        self.client.get(
            "/model/users", params={"model_id": self.model_id}, name="/model/users"
        )

    @task
    def model_costs(self):
        r = self.client.get(
            "/model/costs", params={"model_id": self.model_id}, name="/model/costs"
        )

        new_sheet = r.json()

        self.client.post(
            "/model/costs",
            params={"model_id": self.model_id},
            json=new_sheet,
            name="/model/costs",
        )

    @task
    def model_revenues(self):
        r = self.client.get(
            "/model/revenues",
            params={"model_id": self.model_id},
            name="/model/revenues",
        )

        new_sheet = r.json()

        self.client.post(
            "/model/revenues",
            params={"model_id": self.model_id},
            json=new_sheet,
            name="/model/revenues",
        )

    @task
    def model_payroll(self):
        self.client.get(
            "/model/payroll", params={"model_id": self.model_id}, name="/model/payroll"
        )

    @task
    def model_grant_revoke(self):

        user_darwin = "62bb11835529faba0704639c"

        # revoke admin permission
        self.client.post(
            "/model/grant",
            params={
                "model_id": self.model_id,
                "role": "admin",
                "user_id": user_darwin,
            },
            name="/model/grant",
        )

        # revoke admin role
        self.client.post(
            "/model/revoke",
            params={
                "model_id": self.model_id,
                "role": "admin",
                "user_id": user_darwin,
            },
            name="/model/revoke",
        )

    @task
    def model_rename(self):
        self.client.post(
            "/model/rename",
            params={
                "model_id": self.model_id,
                "name": "new_model_name",
            },
            name="/model/rename",
        )

    @task
    def model_starting_month(self):
        self.client.post(
            "/model/startingMonth",
            params={
                "model_id": self.model_id,
                "starting_month": "2022-01-01",
            },
            name="/model/startingMonth",
        )

    @task
    def model_starting_balance(self):
        self.client.post(
            "/model/startingBalance",
            params={
                "model_id": self.model_id,
                "starting_balance": 12345.67,
            },
            name="/model/startingBalance",
        )

    @task
    def model_add_delete(self):
        workspace_id = "62bc5706a40e85213c27ce29"

        r = self.client.post(
            "/model/add",
            params={
                "name": "my new model",
                "workspace_id": workspace_id,
            },
            name="/model/add",
        )

        model_id = r.json()["_id"]

        self.client.delete(
            "/model",
            params={
                "model_id": model_id,
            },
            name="/model",
        )
