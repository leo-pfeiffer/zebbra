import pytest
from fastapi.testclient import TestClient
from starlette import status

from core.dao.models import get_models_for_workspace
from core.dao.users import get_user
from core.dao.workspaces import get_workspace
from main import app


@pytest.mark.anyio
async def test_get_workspaces_for_user(access_token):
    client = TestClient(app)

    response = client.get(
        "/workspace", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    user = await get_user("johndoe@example.com")
    assert len(response.json()) == len(user.workspaces)
    for w in user.workspaces:
        assert w in [x["name"] for x in response.json()]


@pytest.mark.anyio
async def test_create_new_workspace(access_token):
    client = TestClient(app)

    response = client.post(
        "/workspace?name=my_workspace",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    wsp = await get_workspace("my_workspace")
    assert wsp is not None
    assert wsp.admin == "johndoe@example.com"


@pytest.mark.anyio
async def test_create_new_workspace_duplicate(access_token):
    client = TestClient(app)

    client.post(
        "/workspace?name=my_workspace",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response = client.post(
        "/workspace?name=my_workspace",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_workspace_rename(access_token):
    client = TestClient(app)

    response = client.post(
        "/workspace/rename",
        params={"old_name": "ACME Inc.", "new_name": "foobar"},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert await get_workspace("foobar") is not None
    assert await get_workspace("ACME Inc.") is None


@pytest.mark.anyio
async def test_workspace_rename_exists(access_token):
    client = TestClient(app)

    response = client.post(
        "/workspace/rename",
        params={"old_name": "ACME Inc.", "new_name": "Boring Co."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_workspace_add(access_token):
    client = TestClient(app)

    u = "alice@example.com"
    response = client.post(
        "/workspace/add",
        params={"username": u, "workspace": "ACME Inc."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    wsp = await get_workspace("ACME Inc.")
    assert u in wsp.users
    alice = await get_user(u)
    assert "ACME Inc." in alice.workspaces


@pytest.mark.anyio
async def test_workspace_add_non_existent_user(access_token):
    client = TestClient(app)

    response = client.post(
        "/workspace/add",
        params={"username": "notauser@me.com", "workspace": "ACME Inc."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_workspace_remove(access_token):
    client = TestClient(app)

    u = "charlie@example.com"
    response = client.post(
        "/workspace/remove",
        params={"username": u, "workspace": "ACME Inc."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    wsp = await get_workspace("ACME Inc.")
    assert u not in wsp.users
    charlie = await get_user(u)
    assert "ACME Inc." not in charlie.workspaces


@pytest.mark.anyio
async def test_workspace_remove_user_removes_from_models(access_token):
    client = TestClient(app)

    u = "charlie@example.com"

    response = client.post(
        "/workspace/remove",
        params={"username": u, "workspace": "ACME Inc."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    models = await get_models_for_workspace("ACME Inc.")
    for m in models:
        assert u not in m["meta"]["admins"]
        assert u not in m["meta"]["editors"]
        assert u not in m["meta"]["viewers"]


@pytest.mark.anyio
async def test_workspace_remove_user_cannot_admin(access_token):
    client = TestClient(app)

    u = "johndoe@example.com"

    response = client.post(
        "/workspace/remove",
        params={"username": u, "workspace": "ACME Inc."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_workspace_remove_non_existent_user(access_token):
    client = TestClient(app)

    response = client.post(
        "/workspace/changeAdmin",
        params={"username": "notauser@me.com", "workspace": "ACME Inc."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_workspace_remove_user_not_in_workspace(access_token):
    client = TestClient(app)

    response = client.post(
        "/workspace/changeAdmin",
        params={"username": "alice@example.com", "workspace": "ACME Inc."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_workspace_change_admin(access_token):
    client = TestClient(app)

    response = client.post(
        "/workspace/changeAdmin",
        params={"username": "charlie@example.com", "workspace": "ACME Inc."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    wsp = await get_workspace("ACME Inc.")
    assert wsp.admin == "charlie@example.com"


@pytest.mark.anyio
async def test_get_users_of_workspace(access_token):
    client = TestClient(app)

    response = client.get(
        "/workspace/users",
        params={"name": "ACME Inc."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    unique = set()
    wsp = await get_workspace("ACME Inc.")
    wsp_users = set(wsp.users)
    wsp_users.add(wsp.admin)

    for u in users:
        if u["username"] == "johndoe@example.com":
            assert u["user_role"] == "Admin"
        else:
            assert u["user_role"] == "Member"
        unique.add(u["username"])

        assert u["username"] in wsp_users

    assert len(users) == len(unique)
    assert len(wsp_users) == len(unique)


@pytest.mark.anyio
async def test_get_users_of_workspace_no_access(access_token_alice):
    client = TestClient(app)

    response = client.get(
        "/workspace/users",
        params={"name": "ACME Inc."},
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
