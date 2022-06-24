import pyotp
import pytest
from fastapi.testclient import TestClient
from starlette import status

from core.dao.users import set_user_otp_secret, set_user_otp_secret_validated
from main import app


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
async def test_oauth_with_valid_user_does_with_valid_otp():

    username = "johndoe@example.com"
    secret = pyotp.random_base32()
    await set_user_otp_secret(username, secret)
    await set_user_otp_secret_validated(username)
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
async def test_oauth_with_valid_user_does_with_invalid_otp():

    username = "johndoe@example.com"

    secret = pyotp.random_base32()
    await set_user_otp_secret("johndoe@example.com", secret)
    await set_user_otp_secret_validated(username)

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
