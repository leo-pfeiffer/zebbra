import pyotp
import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from starlette import status

from core.dao.users import (
    set_user_otp_secret,
    set_user_otp_secret_validated,
    get_user_by_username,
    get_user,
)
from core.dao.workspaces import get_workspace, get_workspace_by_name
from core.schemas.users import RegisterUser
from main import app
from tests.utils import count_documents


def test_oauth_with_valid_user():
    user_form = {
        "grant_type": "password",
        "username": "johndoe@example.com",
        "password": "secret",
    }

    client = TestClient(app)
    response = client.post("/token", data=user_form)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.anyio
async def test_oauth_with_valid_user_does_with_valid_otp(users):
    username = "johndoe@example.com"
    secret = pyotp.random_base32()
    await set_user_otp_secret(users[username], secret)
    await set_user_otp_secret_validated(users[username])
    totp = pyotp.TOTP(secret)
    otp = totp.now()

    user_form = {
        "grant_type": "password",
        "username": "johndoe@example.com",
        "password": "secret",
        "otp": otp,
    }

    client = TestClient(app)
    response = client.post("/token", data=user_form)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.anyio
async def test_oauth_with_valid_user_does_with_invalid_otp(users):
    username = "johndoe@example.com"

    secret = pyotp.random_base32()
    await set_user_otp_secret(users[username], secret)
    await set_user_otp_secret_validated(users[username])

    user_form = {
        "grant_type": "password",
        "username": "johndoe@example.com",
        "password": "secret",
    }

    client = TestClient(app)
    response = client.post("/token", data=user_form)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_oauth_with_invalid_user():
    user_form = {
        "grant_type": "password",
        "username": "johndoe@example.com",
        "password": "wrongsecret",
    }

    client = TestClient(app)
    response = client.post("/token", data=user_form)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_register_with_existing_wsp(workspaces):
    new_user_form = RegisterUser(
        **{
            "username": "test_user@example.com",
            "first_name": "Henry",
            "last_name": "Ford",
            "workspace_id": workspaces["ACME Inc."],
            "new_workspace_name": None,
            "password": "secret",
        }
    )

    client = TestClient(app)
    response = client.post("/register", json=jsonable_encoder(new_user_form))

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["username"] == "test_user@example.com"
    user_id = response.json()["_id"]

    user = await get_user(user_id)

    assert user.username == new_user_form.username
    assert user.first_name == new_user_form.first_name
    assert user.last_name == new_user_form.last_name

    workspace = await get_workspace(workspaces["ACME Inc."])
    assert user_id in [str(x) for x in workspace.users]


@pytest.mark.anyio
async def test_register_with_new_wsp(workspaces):
    new_user_form = RegisterUser(
        username="test_user@example.com",
        first_name="Henry",
        last_name="Ford",
        workspace_id=None,
        new_workspace_name="Ford Motors",
        password="secret",
    )

    client = TestClient(app)
    response = client.post("/register", json=jsonable_encoder(new_user_form))

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["username"] == "test_user@example.com"
    user_id = response.json()["_id"]

    user = await get_user(user_id)

    assert user.username == new_user_form.username
    assert user.first_name == new_user_form.first_name
    assert user.last_name == new_user_form.last_name

    workspace = await get_workspace_by_name("Ford Motors")
    assert user_id in [str(x) for x in workspace.users]
    assert user_id in str(workspace.admin)


@pytest.mark.anyio
async def test_register_can_login(workspaces):
    new_user_form = {
        "username": "test_user@example.com",
        "first_name": "Henry",
        "last_name": "Ford",
        "workspace_id": workspaces["ACME Inc."],
        "new_workspace_name": None,
        "password": "secret",
    }

    client = TestClient(app)
    response = client.post("/register", json=jsonable_encoder(new_user_form))

    assert response.status_code == status.HTTP_200_OK

    user_form = {
        "grant_type": "password",
        "username": "test_user@example.com",
        "password": "secret",
    }

    client = TestClient(app)
    response = client.post("/token", data=user_form)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_register_cannot_specify_both_new_workspace_and_existing(workspaces):
    new_user_form = {
        "username": "test_user@example.com",
        "first_name": "Henry",
        "last_name": "Ford",
        "workspace_id": workspaces["ACME Inc."],
        "new_workspace_name": "Ford Motors",
        "password": "secret",
    }

    client = TestClient(app)
    response = client.post("/register", json=jsonable_encoder(new_user_form))

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_register_cannot_specify_neither_new_workspace_and_existing(workspaces):
    new_user_form = {
        "username": "test_user@example.com",
        "first_name": "Henry",
        "last_name": "Ford",
        "password": "secret",
        "workspace_id": None,
        "new_workspace_name": None,
    }

    client = TestClient(app)
    response = client.post("/register", json=jsonable_encoder(new_user_form))

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_cannot_register_existing_username(workspaces):
    user = RegisterUser(
        **{
            "username": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "workspace_id": workspaces["ACME Inc."],
            "new_workspace_name": None,
            "password": "secret",
        }
    )

    users_initial = await count_documents("users")

    client = TestClient(app)
    response = client.post("/register", json=jsonable_encoder(user))

    assert response.status_code == status.HTTP_409_CONFLICT
    assert await count_documents("users") == users_initial
