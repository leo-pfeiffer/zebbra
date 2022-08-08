from locust import HttpUser, task, between

from mixins import JohnDoeMixin


class LocustWorkspaces(JohnDoeMixin, HttpUser):
    wait_time = between(1, 5)
    weight = 10

    workspace_id = "62bc5706a40e85213c27ce29"

    @task
    def model_meta(self):
        self.client.get(
            "/workspace", params={"workspace_id": self.workspace_id}, name="/workspace"
        )

    @task
    def model_users(self):
        self.client.get(
            "/workspace/users",
            params={"workspace_id": self.workspace_id},
            name="/workspace/users",
        )
