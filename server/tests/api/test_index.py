import pytest
from fastapi.testclient import TestClient
from starlette import status

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Zebbra!"}


@pytest.mark.anyio
async def test_logout(access_token):
    response = client.post(
        "/logout", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.json()["message"] == "Logged out."


@pytest.mark.anyio
async def test_cannot_use_token_after_logout(access_token):
    logout_response = client.post(
        "/logout", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert logout_response.json()["message"] == "Logged out."

    test_response = client.get(
        "/user", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert test_response.status_code == status.HTTP_401_UNAUTHORIZED
