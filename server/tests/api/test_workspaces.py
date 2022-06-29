import pytest
from fastapi.testclient import TestClient
from starlette import status

from core.dao.models import get_models_for_workspace
from core.dao.users import get_user
from core.dao.workspaces import get_workspace, get_workspace_by_name
from main import app


@pytest.mark.anyio
async def test_get_workspaces_for_user(access_token, users):
    client = TestClient(app)

    response = client.get(
        "/workspace", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    user = await get_user(users["johndoe@example.com"])
    for w in [x["users"] for x in response.json()]:
        assert str(user.id) in w


@pytest.mark.anyio
async def test_create_new_workspace(access_token, users):
    client = TestClient(app)

    response = client.post(
        "/workspace?name=my_workspace",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    wsp = await get_workspace_by_name("my_workspace")
    assert wsp is not None
    assert str(wsp.admin) == users["johndoe@example.com"]


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
async def test_workspace_rename(access_token, workspaces):
    client = TestClient(app)

    response = client.post(
        "/workspace/rename",
        params={"workspace_id": workspaces["ACME Inc."], "new_name": "foobar"},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert await get_workspace_by_name("foobar") is not None
    assert await get_workspace_by_name("ACME Inc.") is None


@pytest.mark.anyio
async def test_workspace_rename_exists(access_token, workspaces):
    client = TestClient(app)

    response = client.post(
        "/workspace/rename",
        params={"workspace_id": workspaces["ACME Inc."], "new_name": "Boring Co."},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_workspace_add(access_token, users, workspaces):
    client = TestClient(app)

    u = users["alice@example.com"]
    response = client.post(
        "/workspace/add",
        params={"user_id": u, "workspace_id": workspaces["ACME Inc."]},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    wsp = await get_workspace_by_name("ACME Inc.")
    assert u in [str(x) for x in wsp.users]


@pytest.mark.anyio
async def test_workspace_add_non_existent_user(access_token, not_an_id, workspaces):
    client = TestClient(app)

    response = client.post(
        "/workspace/add",
        params={"user_id": not_an_id, "workspace_id": workspaces["ACME Inc."]},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_workspace_remove(access_token, users, workspaces):
    client = TestClient(app)

    u = users["charlie@example.com"]
    response = client.post(
        "/workspace/remove",
        params={"user_id": u, "workspace_id": workspaces["ACME Inc."]},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    wsp = await get_workspace_by_name("ACME Inc.")
    assert u not in [str(x) for x in wsp.users]


@pytest.mark.anyio
async def test_workspace_remove_user_removes_from_models(
    access_token, users, workspaces
):
    client = TestClient(app)

    u = users["charlie@example.com"]

    response = client.post(
        "/workspace/remove",
        params={"user_id": u, "workspace_id": workspaces["ACME Inc."]},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    models = await get_models_for_workspace(workspaces["ACME Inc."])
    for m in models:
        assert u not in m["meta"]["admins"]
        assert u not in m["meta"]["editors"]
        assert u not in m["meta"]["viewers"]


@pytest.mark.anyio
async def test_workspace_remove_user_cannot_admin(access_token, users, workspaces):
    client = TestClient(app)

    u = users["johndoe@example.com"]

    response = client.post(
        "/workspace/remove",
        params={"user_id": u, "workspace_id": workspaces["ACME Inc."]},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_workspace_remove_non_existent_user(access_token, not_an_id, workspaces):
    client = TestClient(app)

    response = client.post(
        "/workspace/changeAdmin",
        params={"user_id": not_an_id, "workspace_id": workspaces["ACME Inc."]},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_workspace_remove_user_not_in_workspace(access_token, users, workspaces):
    client = TestClient(app)

    response = client.post(
        "/workspace/changeAdmin",
        params={
            "user_id": users["alice@example.com"],
            "workspace_id": workspaces["ACME Inc."],
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_workspace_change_admin(access_token, users, workspaces):
    client = TestClient(app)

    u = users["charlie@example.com"]

    response = client.post(
        "/workspace/changeAdmin",
        params={"user_id": u, "workspace_id": workspaces["ACME Inc."]},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    wsp = await get_workspace_by_name("ACME Inc.")
    assert str(wsp.admin) == u


@pytest.mark.anyio
async def test_get_users_of_workspace(access_token, users, workspaces):
    client = TestClient(app)

    response = client.get(
        "/workspace/users",
        params={"workspace_id": workspaces["ACME Inc."]},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    res = response.json()
    unique = set()
    wsp = await get_workspace_by_name("ACME Inc.")
    wsp_users = set([str(x) for x in wsp.users])
    wsp_users.add(str(wsp.admin))

    for u in res:
        if u["username"] == "johndoe@example.com":
            assert u["user_role"] == "Admin"
        else:
            assert u["user_role"] == "Member"
        unique.add(u["username"])

        assert users[u["username"]] in wsp_users

    assert len(res) == len(unique)
    assert len(wsp_users) == len(unique)


@pytest.mark.anyio
async def test_get_users_of_workspace_no_access(access_token_alice, workspaces):
    client = TestClient(app)

    response = client.get(
        "/workspace/users",
        params={"workspace_id": workspaces["ACME Inc."]},
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
