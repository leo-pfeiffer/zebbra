import os

# need this before the other import
# environment variables setup
os.environ['ENV'] = 'test'
os.environ['MONGODB_DB'] = 'zebbra_test'

import pytest
from fastapi.testclient import TestClient
from main import app


# add fixtures here
@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def access_token():
    client = TestClient(app)
    user_form = {
        'grant_type': 'password',
        'username': 'johndoe@example.com',
        'password': 'secret'
    }
    response = client.post("/token", data=user_form)
    return response.json()['access_token']
