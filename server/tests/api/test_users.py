import pytest
from fastapi.testclient import TestClient
from starlette import status

from core.dao.workspaces import change_workspace_admin
from main import app
from tests.utils import assert_unauthorized_login_checked


def test_users_me(access_token):
    client = TestClient(app)
    response = client.get("/user", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "johndoe@example.com"


def test_user_protected():
    assert_unauthorized_login_checked("/user")


def test_user_delete_protected():
    assert_unauthorized_login_checked("/user/delete")


def test_delete_user(access_token_zeus):
    client = TestClient(app)

    response = client.get(
        "/user/delete", headers={"Authorization": f"Bearer {access_token_zeus}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "User deleted."


def test_cannot_delete_user_who_is_workspace_admin(access_token):
    client = TestClient(app)
    response = client.get(
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
    response = client.get(
        "/user/delete", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"].startswith("Attempting to delete model admin")
