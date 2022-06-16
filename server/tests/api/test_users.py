import pytest
from fastapi.testclient import TestClient

from core.models.workspaces import change_workspace_admin
from main import app
from tests.utils import assert_unauthorized_login_checked


def test_users_me(access_token):
    client = TestClient(app)
    response = client.get("/user", headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert response.status_code == 200
    assert response.json()['username'] == 'johndoe@example.com'


def test_users_me_protected():
    assert_unauthorized_login_checked("/user")


@pytest.mark.anyio
async def test_delete_user(access_token):
    client = TestClient(app)

    # make sure current user is no longer an admin
    wsp = "ACME Inc."
    username = "alice@example.com"
    await change_workspace_admin(wsp, username)

    response = client.get("/user/delete", headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert response.status_code == 200
    assert response.json()['message'] == 'User deleted.'


def test_cannot_delete_user_who_is_admin(access_token):
    client = TestClient(app)
    response = client.get("/user/delete", headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert response.status_code == 400
