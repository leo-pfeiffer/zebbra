from locust import HttpUser, task, between

from mixins import JohnDoeMixin


class LocustUser(JohnDoeMixin, HttpUser):
    wait_time = between(1, 5)
    weight = 10

    @task
    def user(self):
        self.client.get(
            "/user",
            name="/user",
        )

    @task
    def user_update(self):
        self.client.post("/user", params={"first_name": "John Stuart"}, name="/user")
