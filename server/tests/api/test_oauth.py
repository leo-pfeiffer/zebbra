import pytest
from fastapi.testclient import TestClient
from main import app


def test_oauth_with_valid_user():

    user_form = {
        'grant_type': 'password',
        'username': 'johndoe',
        'password': 'secret'
    }

    client = TestClient(app)
    response = client.post("/token", data=user_form)

    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'


@pytest.mark.anyio
async def test_oauth_with_invalid_user():

    user_form = {
        'grant_type': 'password',
        'username': 'johndoe',
        'password': 'wrongsecret'
    }

    client = TestClient(app)
    response = client.post("/token", data=user_form)

    assert response.status_code == 401
