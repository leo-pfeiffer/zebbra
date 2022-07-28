class JohnDoeMixin:
    def on_start(self):

        user_form = {
            "grant_type": "password",
            "username": "johndoe@example.com",
            "password": "secret",
        }
        resp = self.client.post("/token", data=user_form)

        self.client.headers.update(
            {"Authorization": f"Bearer {resp.json()['access_token']}"}
        )
