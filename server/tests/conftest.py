import os

# need this before the other import
# environment variables setup
from core.schemas.integrations import IntegrationAccess, IntegrationAccessToken

os.environ["ENV"] = "test"
os.environ["MONGODB_DB"] = "zebbra_test"

import pytest
from fastapi.testclient import TestClient
from main import app
from tests.factory import (
    create,
    teardown,
)


# add fixtures here
@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def mongodb():
    # before test
    await teardown()
    await create()
    yield
    # after test
    await teardown()


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


@pytest.fixture
def users() -> dict:
    return {
        "johndoe@example.com": "62bb11835529faba0704639d",
        "alice@example.com": "62bb11835529faba07046398",
        "bob@example.com": "62bb11835529faba0704639b",
        "charlie@example.com": "62bb11835529faba0704639a",
        "darwin@example.com": "62bb11835529faba0704639c",
        "zeus@example.com": "62bb11835529faba07046399",
    }


@pytest.fixture
def workspaces() -> dict:
    return {
        "Boring Co.": "62bc5706a40e85213c27ce28",
        "ACME Inc.": "62bc5706a40e85213c27ce29",
    }


@pytest.fixture
def not_an_id():
    return "12ab12345678faba1234567d"


@pytest.fixture
def invite_codes() -> dict:
    return {"valid": "never_expires", "expired": "already_expired"}


@pytest.fixture
def expired_xero_token() -> IntegrationAccess:
    return IntegrationAccess(
        workspace_id="62bc5706a40e85213c27ce29",
        integration="Xero",
        token=IntegrationAccessToken(
            id_token="id-token",
            access_token="access-token",
            expires_in=1800,
            token_type="Bearer",
            refresh_token="refresh-token",
            scope="some scope",
            expires_at=1656898425,
        ),
        tenant_id="tenant-id",
    )


@pytest.fixture
def never_expired_xero_token() -> IntegrationAccess:
    return IntegrationAccess(
        workspace_id="62bc5706a40e85213c27ce29",
        integration="Xero",
        token=IntegrationAccessToken(
            id_token="id-token",
            access_token="access-token",
            expires_in=1800,
            token_type="Bearer",
            refresh_token="refresh-token",
            scope="some scope",
            expires_at=3756898425,
        ),
        tenant_id="tenant-id",
    )
