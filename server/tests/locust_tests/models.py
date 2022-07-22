from locust import HttpUser, task, between

from mixins import JohnDoeMixin


class LocustModels(JohnDoeMixin, HttpUser):
    wait_time = between(1, 5)
    weight = 10

    model_id = "62b488ba433720870b60ec0a"

    @task
    def model_meta(self):
        self.client.get("/model/meta", params={"model_id": self.model_id})

    @task
    def model_users(self):
        self.client.get("/model/users", params={"model_id": self.model_id})

    @task
    def model_costs(self):
        self.client.get("/model/costs", params={"model_id": self.model_id})

    @task
    def model_revenues(self):
        self.client.get("/model/revenues", params={"model_id": self.model_id})

    @task
    def model_payroll(self):
        self.client.get("/model/payroll", params={"model_id": self.model_id})
