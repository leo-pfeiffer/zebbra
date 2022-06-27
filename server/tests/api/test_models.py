import pytest
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.testclient import TestClient

from core.dao.models import is_admin, is_editor, is_viewer, get_model_by_id
from core.schemas.sheets import SheetMeta, Section
from main import app
from tests.utils import assert_unauthorized_login_checked


def test_model_protected():
    assert_unauthorized_login_checked("/model")


def test_model_more_than_one_param(access_token):
    client = TestClient(app)
    response = client.get(
        "/model/?user=true&model_id=some_random_id",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_model_no_param(access_token):
    client = TestClient(app)
    response = client.get(
        "/model",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_model_get_by_id(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    response = client.get(
        f"/model/?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["_id"] == model_id


def test_model_get_by_id_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "not a model"
    response = client.get(
        f"/model/?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_model_get_id_forbidden(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0b"
    response = client.get(
        f"/model/?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_model_get_workspace(access_token):
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


def test_model_get_workspace_forbidden(access_token):
    client = TestClient(app)
    wsp = "Boring Co."
    response = client.get(
        f"/model/?workspace={wsp}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_model_user(access_token):
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
        f"/model/grant?model_id={model_id}&role={role}&user={user}",
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
        f"/model/grant?model_id={model_id}&role={role}&user={user}",
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
        f"/model/grant?model_id={model_id}&role={role}&user={user}",
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
        f"/model/grant?model_id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert not await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_grant_permission_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "not a model"
    user = "johndoe@example.com"
    role = "viewer"
    response = client.post(
        f"/model/grant?model_id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_revoke_permission_editor(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = "darwin@example.com"
    role = "editor"

    response = client.post(
        f"/model/revoke?model_id={model_id}&role={role}&user={user}",
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
        f"/model/revoke?model_id={model_id}&role={role}&user={user}",
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
        f"/model/revoke?model_id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_revoke_permission_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "not a model"
    user = "charlie@example.com"
    role = "viewer"
    response = client.post(
        f"/model/revoke?model_id={model_id}&role={role}&user={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_rename_model(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    new_name = "new_name"
    response = client.post(
        f"/model/rename?model_id={model_id}&name={new_name}",
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
        f"/model/rename?model_id={model_id}&name={new_name}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    model = await get_model_by_id(model_id)
    assert model["meta"]["name"] != new_name


@pytest.mark.anyio
async def test_rename_model_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "not a model"
    new_name = "new_name"
    response = client.post(
        f"/model/rename?model_id={model_id}&name={new_name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_add_model(access_token):
    client = TestClient(app)
    new_name = "new_name"
    workspace = "ACME Inc."
    response = client.post(
        f"/model/add?name={new_name}&workspace={workspace}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    model = response.json()
    assert model["meta"]["name"] == new_name
    assert model["meta"]["workspace"] == workspace
    assert model["meta"]["admin"] == "johndoe@example.com"


@pytest.mark.anyio
async def test_add_model_no_access(access_token):
    client = TestClient(app)
    new_name = "new_name"
    workspace = "Boring Co."
    response = client.post(
        f"/model/add?name={new_name}&workspace={workspace}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_update_sheet_meta(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    model1 = await get_model_by_id(model_id)
    old_sheet_name = model1["sheets"][0]["meta"]["name"]
    new_sheet_name = "new sheet name"
    new_meta = SheetMeta(name=new_sheet_name)

    response = client.post(
        f"/model/sheet/update/meta?model_id={model_id}&name={old_sheet_name}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(new_meta),
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["sheets"][0]["meta"]["name"] == new_sheet_name


@pytest.mark.anyio
async def test_update_sheet_meta_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "not a model"
    new_sheet_name = "new sheet name"
    new_meta = SheetMeta(name=new_sheet_name)

    response = client.post(
        f"/model/sheet/update/meta?model_id={model_id}&name=foo",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(new_meta),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_update_sheet_meta_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    model1 = await get_model_by_id(model_id)
    old_sheet_name = model1["sheets"][0]["meta"]["name"]
    new_sheet_name = "new sheet name"
    new_meta = SheetMeta(name=new_sheet_name)

    response = client.post(
        f"/model/sheet/update/meta?model_id={model_id}&name={old_sheet_name}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
        json=jsonable_encoder(new_meta),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_update_sheet_meta_duplicate_name(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    model1 = await get_model_by_id(model_id)
    old_sheet_name = model1["sheets"][0]["meta"]["name"]
    new_meta = SheetMeta(name=old_sheet_name)

    response = client.post(
        f"/model/sheet/update/meta?model_id={model_id}&name={old_sheet_name}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(new_meta),
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.anyio
async def test_update_sheet_data(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    model1 = await get_model_by_id(model_id)
    old_sheet_name = model1["sheets"][0]["meta"]["name"]

    new_data = [
        Section(**{"name": "section1", "rows": [], "end_row": None}),
        Section(**{"name": "section2", "rows": [], "end_row": None}),
    ]

    response = client.post(
        f"/model/sheet/update/data?model_id={model_id}&name={old_sheet_name}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(new_data),
    )

    assert response.status_code == status.HTTP_200_OK

    model2 = response.json()
    assert len(model2["sheets"][0]["sections"]) == 2
    assert model2["sheets"][0]["sections"][0]["name"] == "section1"
    assert model2["sheets"][0]["sections"][1]["name"] == "section2"


@pytest.mark.anyio
async def test_update_sheet_data_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    model1 = await get_model_by_id(model_id)
    old_sheet_name = model1["sheets"][0]["meta"]["name"]

    response = client.post(
        f"/model/sheet/update/data?model_id={model_id}&name={old_sheet_name}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
        json=jsonable_encoder([]),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_update_sheet_data_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "not a model"

    response = client.post(
        f"/model/sheet/update/data?model_id={model_id}&name=foo",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder([]),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
