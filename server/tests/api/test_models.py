import pytest
from starlette import status
from starlette.testclient import TestClient

from core.dao.models import is_admin, is_editor, is_viewer, get_model_by_id
from main import app
from tests.utils import assert_unauthorized_login_checked


def test_model_protected():
    assert_unauthorized_login_checked("/model")


def test_more_than_one_param(access_token):
    client = TestClient(app)
    response = client.get(
        "/model/?user=true&id=some_random_id",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_no_param(access_token):
    client = TestClient(app)
    response = client.get(
        "/model",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_by_id(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    response = client.get(
        f"/model/?id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["_id"] == model_id


def test_get_id_forbidden(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0b"
    response = client.get(
        f"/model/?id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_workspace(access_token):
    client = TestClient(app)
    wsp = "ACME Inc."
    response = client.get(
        f"/model/?workspace={wsp}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 1
    for m in response.json():
        assert m["meta"]["workspace"] == wsp


def test_get_workspace_forbidden(access_token):
    client = TestClient(app)
    wsp = "Boring Co."
    response = client.get(
        f"/model/?workspace={wsp}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_user(access_token):
    client = TestClient(app)
    response = client.get(
        f"/model/?user=true",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    user = "johndoe@example.com"
    for m in response.json():
        assert (
            (m["meta"]["admin"] == user)
            or (user in m["meta"]["editors"])
            or (user in m["meta"]["viewers"])
        )


@pytest.mark.anyio
async def test_grant_permission_admin(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = "darwin@example.com"
    role = "admin"
    response = client.post(
        f"/model/grant?id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Access granted (admin)"

    assert await is_admin(model_id, user)


@pytest.mark.anyio
async def test_grant_permission_editor(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = "johndoe@example.com"
    role = "editor"
    response = client.post(
        f"/model/grant?id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Access granted (editor)"

    assert await is_editor(model_id, user)


@pytest.mark.anyio
async def test_grant_permission_viewer(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = "johndoe@example.com"
    role = "viewer"
    response = client.post(
        f"/model/grant?id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Access granted (viewer)"

    assert await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_grant_permission_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = "johndoe@example.com"
    role = "viewer"
    response = client.post(
        f"/model/grant?id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert not await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_revoke_permission_editor(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = "darwin@example.com"
    role = "editor"

    response = client.post(
        f"/model/revoke?id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Access revoked (editor)"

    assert not await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_revoke_permission_viewer(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = "charlie@example.com"
    role = "viewer"
    response = client.post(
        f"/model/revoke?id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Access revoked (viewer)"

    assert not await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_revoke_permission_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = "charlie@example.com"
    role = "viewer"
    response = client.post(
        f"/model/revoke?id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_rename_model(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    new_name = "new_name"
    response = client.post(
        f"/model/rename?id={model_id}&name={new_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Model renamed ({new_name})"

    model = await get_model_by_id(model_id)
    assert model["meta"]["name"] == new_name


@pytest.mark.anyio
async def test_rename_model_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    new_name = "new_name"
    response = client.post(
        f"/model/rename?id={model_id}&name={new_name}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    model = await get_model_by_id(model_id)
    assert model["meta"]["name"] != new_name


#
# def test_(access_token):
#     assert False
#
#
# def test_(access_token):
#     assert False
#
#
# def test_(access_token):
#     assert False
