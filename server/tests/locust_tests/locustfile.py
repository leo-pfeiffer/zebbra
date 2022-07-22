from locust import HttpUser, between, task

# noinspection PyUnresolvedReferences
from users import LocustUser

# noinspection PyUnresolvedReferences
from models import LocustModels

# noinspection PyUnresolvedReferences
from workspaces import LocustWorkspaces

# noinspection PyUnresolvedReferences
from integrations import LocustIntegrations


class BaselineTest(HttpUser):
    wait_time = between(1, 5)
    weight = 1

    @task(1)
    def baseline(self):
        self.client.get("/")
