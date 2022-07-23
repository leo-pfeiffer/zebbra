from locust import HttpUser, task, between

from mixins import JohnDoeMixin


class LocustIntegrations(JohnDoeMixin, HttpUser):
    wait_time = between(1, 5)
    weight = 10

    workspace_id = "62bc5706a40e85213c27ce29"
    model_id = "62b488ba433720870b60ec0a"

    @task
    def integration_data_endpoints(self):
        self.client.get(
            "/integration/dataEndpoints", params={"model_id": self.model_id}
        )

    @task
    def model_users(self):
        self.client.get(
            "/integration/providers", params={"workspace_id": self.workspace_id}
        )
