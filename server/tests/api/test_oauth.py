import pytest
from fastapi.testclient import TestClient
from starlette import status

from main import app


def test_oauth_with_valid_user():

    user_form = {
        'grant_type': 'password',
        'username': 'johndoe@example.com',
        'password': 'secret'
    }

    client = TestClient(app)
    response = client.post("/token", data=user_form)

    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'


@pytest.mark.anyio
async def test_oauth_with_invalid_user():

    user_form = {
        'grant_type': 'password',
        'username': 'johndoe@example.com',
        'password': 'wrongsecret'
    }

    client = TestClient(app)
    response = client.post("/token", data=user_form)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
