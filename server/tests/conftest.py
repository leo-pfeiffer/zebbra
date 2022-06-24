import os

# need this before the other import
# environment variables setup
os.environ["ENV"] = "test"
os.environ["MONGODB_DB"] = "zebbra_test"

import pytest
from fastapi.testclient import TestClient
from main import app
from tests.factory import (
    create_user_data,
    create_workspace_data,
    create_model_data,
    teardown_users,
    teardown_workspaces,
    teardown_token_blacklist,
    teardown_models,
)


# add fixtures here
@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def mongodb():
    # before test
    await create_user_data()
    await create_workspace_data()
    await create_model_data()
    yield
    # after test
    await teardown_users()
    await teardown_workspaces()
    await teardown_token_blacklist()
    await teardown_models()


@pytest.fixture
def access_token():
    client = TestClient(app)
    user_form = {
        "grant_type": "password",
        "username": "johndoe@example.com",
        "password": "secret",
    }
    response = client.post("/token", data=user_form)
    return response.json()["access_token"]


@pytest.fixture
def access_token_alice():
    client = TestClient(app)
    user_form = {
        "grant_type": "password",
        "username": "alice@example.com",
        "password": "secret",
    }
    response = client.post("/token", data=user_form)
    return response.json()["access_token"]


@pytest.fixture
def access_token_zeus():
    client = TestClient(app)
    user_form = {
        "grant_type": "password",
        "username": "zeus@example.com",
        "password": "secret",
    }
    response = client.post("/token", data=user_form)
    return response.json()["access_token"]
