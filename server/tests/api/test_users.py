import pyotp
import pytest
from fastapi.testclient import TestClient
from starlette import status

from core.dao.models import get_models_for_user
from core.dao.users import get_user, set_user_otp_secret
from core.dao.workspaces import change_workspace_admin, get_workspaces_of_user
from dependencies import get_password_hash
from main import app
from tests.utils import assert_unauthorized_login_checked


def test_users_me(access_token):
    client = TestClient(app)
    response = client.get("/user", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "johndoe@example.com"


def test_user_protected():
    assert_unauthorized_login_checked("/user")


def test_delete_user(access_token_zeus):
    client = TestClient(app)

    response = client.post(
        "/user/delete", headers={"Authorization": f"Bearer {access_token_zeus}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "User deleted."


def test_cannot_delete_user_who_is_workspace_admin(access_token):
    client = TestClient(app)
    response = client.post(
        "/user/delete", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"].startswith("Attempting to delete workspace admin")


@pytest.mark.anyio
async def test_cannot_delete_user_who_is_model_admin(access_token):
    # make sure current user is no longer an admin
    wsp = "ACME Inc."
    username = "alice@example.com"
    await change_workspace_admin(wsp, username)

    client = TestClient(app)
    response = client.post(
        "/user/delete", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"].startswith("Attempting to delete model admin")


@pytest.mark.anyio
async def test_create_otp(access_token):
    client = TestClient(app)
    response = client.post(
        "/user/otp/create", headers={"Authorization": f"Bearer {access_token}"}
    )
    user = await get_user("johndoe@example.com")
    assert user.otp_secret == response.json()["secret"]


@pytest.mark.anyio
async def test_validate_otp_true(access_token):
    client = TestClient(app)

    secret = pyotp.random_base32()
    await set_user_otp_secret("johndoe@example.com", secret)

    totp = pyotp.TOTP(secret)
    otp = totp.now()

    response = client.post(
        f"/user/otp/validate?otp={otp}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.json()["valid"]


@pytest.mark.anyio
async def test_validate_otp_sets_validated_true(access_token):
    client = TestClient(app)

    secret = pyotp.random_base32()
    await set_user_otp_secret("johndoe@example.com", secret)

    totp = pyotp.TOTP(secret)
    otp = totp.now()

    client.post(
        f"/user/otp/validate?otp={otp}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    user = await get_user("johndoe@example.com")
    assert user.otp_validated


@pytest.mark.anyio
async def test_validate_otp_false(access_token):
    client = TestClient(app)

    await set_user_otp_secret("johndoe@example.com", pyotp.random_base32())

    otp = "not the right secret"

    response = client.post(
        f"/user/otp/validate?otp={otp}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert not response.json()["valid"]


@pytest.mark.anyio
async def test_update_username(access_token):
    client = TestClient(app)

    username = "johndoe@example.com"
    new_username = "nolongerjohn@example.com"

    response = client.post(
        f"/user/update?username={new_username}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == new_username

    assert await get_user(new_username) is not None
    assert await get_user(username) is None

    assert len(await get_workspaces_of_user(username)) == 0
    assert len(await get_models_for_user(username)) == 0


@pytest.mark.anyio
async def test_update_username_duplicate(access_token):
    new_username = "alice@example.com"

    client = TestClient(app)

    response = client.post(
        f"/user/update?username={new_username}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_update_first_name(access_token):
    username = "johndoe@example.com"
    first_name = "Alfred"
    client = TestClient(app)

    response = client.post(
        f"/user/update?first_name={first_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == first_name

    user = await get_user(username)
    assert user.first_name == first_name


@pytest.mark.anyio
async def test_update_last_name(access_token):
    username = "johndoe@example.com"
    value = "Hitchcock"

    client = TestClient(app)

    response = client.post(
        f"/user/update?last_name={value}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["last_name"] == value

    user = await get_user(username)
    assert user.last_name == value


@pytest.mark.anyio
async def test_update_password(access_token):
    username = "johndoe@example.com"
    value = "secret"

    client = TestClient(app)

    user_before = await get_user(username)

    response = client.post(
        f"/user/update?password={value}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    user_after = await get_user(username)
    assert user_before.hashed_password != user_after.hashed_password
