from copy import deepcopy
from datetime import date

import pytest
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.testclient import TestClient

from core.dao.models import (
    is_admin,
    is_editor,
    is_viewer,
    get_model_by_id,
    add_admin_to_model,
    get_revenues_sheet,
    get_costs_sheet,
)
from core.schemas.models import ModelMeta, Employee
from core.schemas.sheets import Sheet
from main import app
from tests.utils import assert_unauthorized_login_checked


def test_model_meta_protected():
    assert_unauthorized_login_checked("/model/meta")


@pytest.mark.anyio
async def test_model_meta_get_by_id(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    response = client.get(
        f"/model/meta?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    model = await get_model_by_id(model_id)

    assert ModelMeta(**response.json()) == model.meta


def test_model_meta_get_by_id_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "not a model"
    response = client.get(
        f"/model/meta?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_model_meta_get_id_forbidden(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0b"
    response = client.get(
        f"/model/meta?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_grant_permission_admin(access_token, users):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = users["darwin@example.com"]
    role = "admin"
    response = client.post(
        f"/model/grant?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Access granted (admin)"

    assert await is_admin(model_id, user)


@pytest.mark.anyio
async def test_grant_permission_editor(access_token, users):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = users["johndoe@example.com"]
    role = "editor"
    response = client.post(
        f"/model/grant?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Access granted (editor)"

    assert await is_editor(model_id, user)


@pytest.mark.anyio
async def test_grant_permission_viewer(access_token, users):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = users["johndoe@example.com"]
    role = "viewer"
    response = client.post(
        f"/model/grant?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Access granted (viewer)"

    assert await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_grant_permission_no_access(access_token_alice, users):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = users["johndoe@example.com"]
    role = "viewer"
    response = client.post(
        f"/model/grant?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert not await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_grant_permission_non_existent_model(access_token, users):
    client = TestClient(app)
    model_id = "not a model"
    user = users["johndoe@example.com"]
    role = "viewer"
    response = client.post(
        f"/model/grant?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_revoke_permission_editor(access_token, users):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = users["darwin@example.com"]
    role = "editor"

    response = client.post(
        f"/model/revoke?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Access revoked (editor)"

    assert not await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_revoke_permission_viewer(access_token, users):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = users["charlie@example.com"]
    role = "viewer"
    response = client.post(
        f"/model/revoke?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Access revoked (viewer)"

    assert not await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_revoke_permission_admin(access_token, users):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = users["charlie@example.com"]
    role = "admin"

    await add_admin_to_model(user, model_id)
    assert await is_admin(model_id, user)

    response = client.post(
        f"/model/revoke?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert not await is_admin(model_id, user)


@pytest.mark.anyio
async def test_revoke_permission_admin_no_admins_left(access_token, users):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = users["johndoe@example.com"]
    role = "admin"
    response = client.post(
        f"/model/revoke?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert await is_admin(model_id, user)


@pytest.mark.anyio
async def test_revoke_permission_admin_workspace_admin(access_token, users):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = users["johndoe@example.com"]
    dummy_user = users["charlie@example.com"]
    role = "admin"

    await add_admin_to_model(dummy_user, model_id)
    assert await is_admin(model_id, dummy_user)

    response = client.post(
        f"/model/revoke?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert await is_admin(model_id, user)


@pytest.mark.anyio
async def test_revoke_permission_no_access(access_token_alice, users):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    user = users["charlie@example.com"]
    role = "viewer"
    response = client.post(
        f"/model/revoke?model_id={model_id}&role={role}&user_id={user}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_revoke_permission_non_existent_model(access_token, users):
    client = TestClient(app)
    model_id = "not a model"
    user = users["charlie@example.com"]
    role = "viewer"
    response = client.post(
        f"/model/revoke?model_id={model_id}&role={role}&user_id={user}",
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
    assert model.meta.name == new_name


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
    assert model.meta.name != new_name


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
async def test_starting_month_model(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    new_date = "2030-12-31"
    response = client.post(
        f"/model/startingMonth?model_id={model_id}&starting_month={new_date}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Starting month set ({new_date})"

    model = await get_model_by_id(model_id)
    assert model.meta.starting_month == date(2030, 12, 31)


@pytest.mark.anyio
async def test_starting_month_model_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    new_date = "2030-12-31"
    response = client.post(
        f"/model/startingMonth?model_id={model_id}&starting_month={new_date}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    model = await get_model_by_id(model_id)
    assert model.meta.starting_month != date(2030, 12, 31)


@pytest.mark.anyio
async def test_starting_month_model_non_existent(access_token):
    client = TestClient(app)
    model_id = "notAModel"
    new_date = "2030-12-31"
    response = client.post(
        f"/model/startingMonth?model_id={model_id}&starting_month={new_date}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_add_model(access_token, users, workspaces):
    client = TestClient(app)
    new_name = "new_name"
    workspace = workspaces["ACME Inc."]
    response = client.post(
        f"/model/add?name={new_name}&workspace_id={workspace}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    model = response.json()
    assert model["meta"]["name"] == new_name
    assert model["meta"]["workspace"] == workspace
    assert users["johndoe@example.com"] in model["meta"]["admins"]


@pytest.mark.anyio
async def test_add_model_no_access(access_token, workspaces):
    client = TestClient(app)
    new_name = "new_name"
    workspace = workspaces["Boring Co."]
    response = client.post(
        f"/model/add?name={new_name}&workspace_id={workspace}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_post_model_revenues(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    sheet = await get_revenues_sheet(model_id)
    sheet_new = Sheet(**sheet.dict())
    for sec in sheet_new.sections:
        sec.name = sec.name + "_changed"

    response = client.post(
        f"/model/revenues?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(sheet_new),
    )

    assert response.status_code == status.HTTP_200_OK

    sheet2 = response.json()
    assert len(sheet2["sections"]) == 1

    for sec in sheet2["sections"]:
        assert sec["name"].endswith("_changed")


@pytest.mark.anyio
async def test_post_model_revenues_contains_integration_values(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    sheet = await get_revenues_sheet(model_id)
    sheet_new = Sheet(**sheet.dict())
    for sec in sheet_new.sections:
        sec.name = sec.name + "_changed"

    response = client.post(
        f"/model/revenues?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(sheet_new),
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["sections"][0]["rows"][1]["integration_values"] is not None
    assert len(response.json()["sections"][0]["rows"][1]["integration_values"]) > 0


@pytest.mark.anyio
async def test_post_model_revenues_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    sheet = await get_revenues_sheet(model_id)

    response = client.post(
        f"/model/revenues?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
        json=jsonable_encoder(sheet),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_post_model_costs(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    sheet = await get_costs_sheet(model_id)
    sheet_new = Sheet(**sheet.dict())
    for sec in sheet_new.sections:
        sec.name = sec.name + "_changed"

    response = client.post(
        f"/model/costs?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(sheet_new),
    )

    assert response.status_code == status.HTTP_200_OK

    sheet2 = response.json()
    assert len(sheet2["sections"]) == 1

    for sec in sheet2["sections"]:
        assert sec["name"].endswith("_changed")


@pytest.mark.anyio
async def test_post_model_costs_contains_integration_values(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    sheet = await get_costs_sheet(model_id)
    sheet_new = Sheet(**sheet.dict())
    for sec in sheet_new.sections:
        sec.name = sec.name + "_changed"

    response = client.post(
        f"/model/costs?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(sheet_new),
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["sections"][0]["rows"][1]["integration_values"] is not None
    assert len(response.json()["sections"][0]["rows"][1]["integration_values"]) > 0


@pytest.mark.anyio
async def test_post_model_costs_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    sheet = await get_revenues_sheet(model_id)

    response = client.post(
        f"/model/costs?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
        json=jsonable_encoder(sheet),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_post_model_costs_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "not-a-model"
    real_model_id = "62b488ba433720870b60ec0a"

    sheet = await get_costs_sheet(real_model_id)

    response = client.post(
        f"/model/costs?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(sheet),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_post_model_revenues_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "not-a-model"
    real_model_id = "62b488ba433720870b60ec0a"

    sheet = await get_revenues_sheet(real_model_id)

    response = client.post(
        f"/model/revenues?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(sheet),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_get_model_revenues(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    response = client.get(
        f"/model/revenues?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["meta"]["name"] == "Revenues"


@pytest.mark.anyio
async def test_get_model_revenues_contains_integration_values(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    response = client.get(
        f"/model/revenues?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["sections"][0]["rows"][1]["integration_values"] is not None
    assert len(response.json()["sections"][0]["rows"][1]["integration_values"]) > 0


@pytest.mark.anyio
async def test_get_model_revenues_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    response = client.get(
        f"/model/revenues?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_get_model_revenues_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "foobar"

    response = client.get(
        f"/model/revenues?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_get_model_costs(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    response = client.get(
        f"/model/costs?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["meta"]["name"] == "Costs"


@pytest.mark.anyio
async def test_get_model_costs_contains_integration_values(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    response = client.get(
        f"/model/costs?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["sections"][0]["rows"][1]["integration_values"] is not None
    assert len(response.json()["sections"][0]["rows"][1]["integration_values"]) > 0


@pytest.mark.anyio
async def test_get_model_costs_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    response = client.get(
        f"/model/costs?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_get_model_costs_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "foobar"

    response = client.get(
        f"/model/costs?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_get_users_of_model(access_token, users):
    model_id = "62b488ba433720870b60ec0a"

    client = TestClient(app)

    response = client.get(
        f"/model/users?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder([]),
    )

    assert response.status_code == status.HTTP_200_OK

    res = response.json()

    unique = set()
    model = await get_model_by_id(model_id)

    admin_set = set([str(x) for x in model.meta.admins])
    editor_set = set([str(x) for x in model.meta.editors])
    viewer_set = set([str(x) for x in model.meta.viewers])

    usernames = list(admin_set.union(editor_set).union(viewer_set))

    for u in res:
        if u["username"] == "johndoe@example.com":
            assert u["user_role"] == "Admin"

        if u["user_role"] == "Admin":
            assert users[u["username"]] in admin_set
        elif u["user_role"] == "Editor":
            assert users[u["username"]] in editor_set
        elif u["user_role"] == "Viewer":
            assert users[u["username"]] in viewer_set

        unique.add(u["username"])

        assert users[u["username"]] in usernames

    assert len(res) == len(unique)
    assert len(usernames) == len(unique)


@pytest.mark.anyio
async def test_get_users_for_model_model_non_existent(access_token):
    model_id = "not_a_model"
    client = TestClient(app)

    response = client.get(
        f"/model/users?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder([]),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_post_model_employees(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    model = await get_model_by_id(model_id)
    employees = deepcopy(model.payroll.employees)
    length_before = len(employees)
    employees.append(
        Employee(
            **{
                "_id": "101",
                "name": "Saint West",
                "start_date": "2021-07-12",
                "end_date": None,
                "title": "COO",
                "department": "Operations",
                "monthly_salary": 3810,
                "from_integration": False,
            }
        )
    )

    response = client.post(
        f"/model/payroll?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(employees),
    )

    assert response.status_code == status.HTTP_200_OK

    model_afterwards = response.json()
    ct = 0
    ct_after = 0
    for e in model_afterwards:
        if e["name"] == "Saint West":
            ct += 1
        elif not e["from_integration"]:
            ct_after += 1

    assert ct == 1
    assert ct_after == length_before


@pytest.mark.anyio
async def test_post_model_employees_ignore_integration(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    model = await get_model_by_id(model_id)
    employees = deepcopy(model.payroll.employees)
    length_before = len(employees)
    employees.append(
        Employee(
            **{
                "_id": "101",
                "name": "Saint West",
                "start_date": "2021-07-12",
                "end_date": None,
                "title": "COO",
                "department": "Operations",
                "monthly_salary": 3810,
                "from_integration": True,
            }
        )
    )

    response = client.post(
        f"/model/payroll?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(employees),
    )

    assert response.status_code == status.HTTP_200_OK

    model_afterwards = response.json()
    ct = 0
    ct_after = 0
    for e in model_afterwards:
        if e["name"] == "Saint West":
            ct += 1
        elif not e["from_integration"]:
            ct_after += 1

    assert ct == 0
    assert ct_after == length_before


@pytest.mark.anyio
async def test_post_model_employees_contains_integration_values(access_token):  # todo
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    model = await get_model_by_id(model_id)

    response = client.post(
        f"/model/payroll?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(model.payroll.employees),
    )

    assert response.status_code == status.HTTP_200_OK
    ct = 0
    for e in response.json():
        if e["from_integration"]:
            ct += 1
    assert ct > 0


@pytest.mark.anyio
async def test_post_model_employees_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    model = await get_model_by_id(model_id)
    employees = deepcopy(model.payroll.employees)
    length_before = len(employees)

    response = client.post(
        f"/model/payroll?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
        json=jsonable_encoder(employees),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    model_after = await get_model_by_id(model_id)
    employees_after = deepcopy(model_after.payroll.employees)
    length_after = len(employees_after)
    assert length_after == length_before


@pytest.mark.anyio
async def test_post_model_employees_non_existent_model(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    model = await get_model_by_id(model_id)

    response = client.post(
        f"/model/payroll?model_id=NOT-A-MODEL",
        headers={"Authorization": f"Bearer {access_token}"},
        json=jsonable_encoder(model.payroll.employees),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_get_model_employees(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    response = client.get(
        f"/model/payroll?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    for e in response.json():
        assert Employee(**e)


@pytest.mark.anyio
async def test_get_model_employees_contains_integration_values(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    response = client.get(
        f"/model/payroll?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    ct = 0
    for e in response.json():
        if e["from_integration"]:
            ct += 1
    assert ct > 0


@pytest.mark.anyio
async def test_get_model_employees_no_access(access_token_alice):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"

    response = client.get(
        f"/model/payroll?model_id={model_id}",
        headers={"Authorization": f"Bearer {access_token_alice}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_get_model_employees_non_existent_model(access_token):
    client = TestClient(app)

    response = client.get(
        f"/model/payroll?model_id=NOT-A-MODEL",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
