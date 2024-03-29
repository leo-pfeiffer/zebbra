from copy import deepcopy

import pytest

from core.dao.models import (
    has_access_to_model,
    get_model_by_id,
    get_models_for_workspace,
    get_models_for_user,
    is_admin,
    is_editor,
    is_viewer,
    add_admin_to_model,
    add_editor_to_model,
    add_viewer_to_model,
    set_name,
    create_model,
    get_users_for_model,
    get_revenues_sheet,
    get_costs_sheet,
    update_costs_sheet,
    update_revenues_sheet,
    set_starting_month,
    update_model_employees,
    delete_model,
    remove_user_from_model, set_starting_balance,
)
from core.dao.workspaces import get_workspace, get_demo_model
from core.exceptions import (
    DoesNotExistException,
    NoAccessException,
    BusinessLogicException,
    CardinalityConstraintFailedException,
)
from datetime import date

from core.schemas.models import Employee, create_new_demo_model
from core.schemas.sheets import Sheet


@pytest.mark.anyio
async def test_delete_model():
    model_id = "62b488ba433720870b60ec0a"
    assert await delete_model(model_id)
    assert await get_model_by_id(model_id) is None


@pytest.mark.anyio
async def test_has_access_to_model_admin(users):
    assert await has_access_to_model(
        "62b488ba433720870b60ec0a", users["johndoe@example.com"]
    )


@pytest.mark.anyio
async def test_has_access_to_model_editor(users):
    assert await has_access_to_model(
        "62b488ba433720870b60ec0a", users["darwin@example.com"]
    )


@pytest.mark.anyio
async def test_has_access_to_model_viewer(users):
    assert await has_access_to_model(
        "62b488ba433720870b60ec0a", users["charlie@example.com"]
    )


@pytest.mark.anyio
async def test_has_access_to_model_false(users):
    assert not await has_access_to_model(
        "62b488ba433720870b60ec0a", users["bob@example.com"]
    )


@pytest.mark.anyio
async def test_get_model_by_id():
    model_id = "62b488ba433720870b60ec0a"
    model = await get_model_by_id(model_id)
    assert str(model.id) == model_id


@pytest.mark.anyio
async def test_get_model_by_id_no_results():
    model_id = "not_an_id"
    assert await get_model_by_id(model_id) is None


@pytest.mark.anyio
async def test_get_models_for_workspace(workspaces):
    wsp = workspaces["ACME Inc."]
    models = await get_models_for_workspace(wsp)
    assert len(models) == 1
    for m in models:
        assert str(m.meta.workspace) == wsp


@pytest.mark.anyio
async def test_get_models_for_workspace_no_results(not_an_id):
    models = await get_models_for_workspace(not_an_id)
    assert len(models) == 0


@pytest.mark.anyio
async def test_get_models_for_user_admin(users):
    u = users["johndoe@example.com"]
    models = await get_models_for_user(u)
    assert len(models) == 1
    for m in models:
        assert u in [str(x) for x in m.meta.admins]


@pytest.mark.anyio
async def test_get_models_for_user_editor(users):
    user = users["darwin@example.com"]
    models = await get_models_for_user(user)
    assert len(models) == 1
    for m in models:
        assert user in [str(x) for x in m.meta.editors]


@pytest.mark.anyio
async def test_get_models_for_user_viewer(users):
    user = users["charlie@example.com"]
    models = await get_models_for_user(user)
    assert len(models) == 1
    for m in models:
        assert user in [str(x) for x in m.meta.viewers]


@pytest.mark.anyio
async def test_get_models_for_user_no_results(not_an_id):
    models = await get_models_for_user(not_an_id)
    assert len(models) == 0


@pytest.mark.anyio
async def test_is_admin_true(users):
    assert await is_admin("62b488ba433720870b60ec0a", users["johndoe@example.com"])


@pytest.mark.anyio
async def test_is_admin_false(users):
    assert not await is_admin("62b488ba433720870b60ec0a", users["darwin@example.com"])


@pytest.mark.anyio
async def test_is_editor_true(users):
    assert await is_editor("62b488ba433720870b60ec0a", users["darwin@example.com"])


@pytest.mark.anyio
async def test_is_editor_false(users):
    assert not await is_editor("62b488ba433720870b60ec0a", users["charlie@example.com"])


@pytest.mark.anyio
async def test_is_viewer_true(users):
    assert await is_viewer("62b488ba433720870b60ec0a", users["charlie@example.com"])


@pytest.mark.anyio
async def test_is_viewer_false(users):
    assert not await is_viewer("62b488ba433720870b60ec0a", users["darwin@example.com"])


@pytest.mark.anyio
async def test_add_admin(users):
    user = users["charlie@example.com"]
    model_id = "62b488ba433720870b60ec0a"
    assert not await is_admin(model_id, user)
    await add_admin_to_model(user, model_id)
    assert await is_admin(model_id, user)


@pytest.mark.anyio
async def test_add_admin_idempotent(users):
    model_id = "62b488ba433720870b60ec0a"
    user = users["charlie@example.com"]
    assert not await is_admin(model_id, user)

    await add_admin_to_model(user, model_id)
    await add_admin_to_model(user, model_id)

    assert await is_admin(model_id, user)
    model = await get_model_by_id(model_id)
    assert (len([str(x) for x in model.meta.admins if str(x) == user])) == 1


@pytest.mark.anyio
async def test_add_admin_removes_previous_role(users):
    model_id = "62b488ba433720870b60ec0a"
    user = users["charlie@example.com"]
    assert not await is_admin(model_id, user)

    await add_editor_to_model(user, model_id)
    await add_admin_to_model(user, model_id)

    assert await is_admin(model_id, user)
    assert not await is_editor(model_id, user)


@pytest.mark.anyio
async def test_add_admin_non_existing_user(not_an_id):
    with pytest.raises(DoesNotExistException):
        await add_admin_to_model(not_an_id, "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_add_editor_to_model(users):
    user = users["charlie@example.com"]
    model_id = "62b488ba433720870b60ec0a"
    assert not await is_editor(model_id, user)
    await add_editor_to_model(user, model_id)
    assert await is_editor(model_id, user)


@pytest.mark.anyio
async def test_add_editor_to_model_idempotent(users):
    model_id = "62b488ba433720870b60ec0a"
    user = users["charlie@example.com"]
    assert not await is_editor(model_id, user)

    await add_editor_to_model(user, model_id)
    await add_editor_to_model(user, model_id)

    assert await is_editor(model_id, user)
    model = await get_model_by_id(model_id)
    assert (len([str(x) for x in model.meta.editors if str(x) == user])) == 1


@pytest.mark.anyio
async def test_add_editor_removes_previous_role(users):
    model_id = "62b488ba433720870b60ec0a"
    user = users["charlie@example.com"]
    assert not await is_editor(model_id, user)

    await add_viewer_to_model(user, model_id)
    await add_editor_to_model(user, model_id)

    assert await is_editor(model_id, user)
    assert not await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_add_editor_to_model_non_existing_user(not_an_id):
    with pytest.raises(DoesNotExistException):
        await add_editor_to_model(not_an_id, "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_add_viewer_to_model(users):
    user = users["darwin@example.com"]
    model_id = "62b488ba433720870b60ec0a"
    assert not await is_viewer(model_id, user)
    await add_viewer_to_model(user, model_id)
    assert await is_viewer(model_id, user)


@pytest.mark.anyio
async def test_add_viewer_to_model_idempotent(users):
    model_id = "62b488ba433720870b60ec0a"
    user = users["darwin@example.com"]

    assert not await is_viewer(model_id, user)

    await add_viewer_to_model(user, model_id)
    await add_viewer_to_model(user, model_id)

    assert await is_viewer(model_id, user)
    model = await get_model_by_id(model_id)
    assert (len([str(x) for x in model.meta.viewers if str(x) == user])) == 1


@pytest.mark.anyio
async def test_add_viewer_removes_previous_role(users):
    model_id = "62b488ba433720870b60ec0a"
    user = users["darwin@example.com"]

    assert not await is_viewer(model_id, user)

    await add_editor_to_model(user, model_id)
    await add_viewer_to_model(user, model_id)

    assert await is_viewer(model_id, user)
    assert not await is_editor(model_id, user)


@pytest.mark.anyio
async def test_add_viewer_to_model_non_existing_user(not_an_id):
    with pytest.raises(DoesNotExistException):
        await add_viewer_to_model(not_an_id, "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_remove_viewer_from_model(users):
    assert await is_viewer("62b488ba433720870b60ec0a", users["charlie@example.com"])
    await remove_user_from_model(
        users["charlie@example.com"], "62b488ba433720870b60ec0a"
    )
    assert not await is_viewer("62b488ba433720870b60ec0a", users["charlie@example.com"])


@pytest.mark.anyio
async def test_remove_viewer_from_model_non_existing_user(not_an_id):
    with pytest.raises(DoesNotExistException):
        await remove_user_from_model(not_an_id, "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_remove_admin_from_model(users):
    await add_admin_to_model(users["charlie@example.com"], "62b488ba433720870b60ec0a")
    assert await is_admin("62b488ba433720870b60ec0a", users["charlie@example.com"])
    await remove_user_from_model(
        users["charlie@example.com"], "62b488ba433720870b60ec0a"
    )
    assert not await is_admin("62b488ba433720870b60ec0a", users["charlie@example.com"])


@pytest.mark.anyio
async def test_remove_admin_from_model_non_existing_user(not_an_id):
    with pytest.raises(DoesNotExistException):
        await remove_user_from_model(not_an_id, "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_remove_admin_from_model_only_one_admin(users):
    with pytest.raises(CardinalityConstraintFailedException):
        await remove_user_from_model(
            users["johndoe@example.com"], "62b488ba433720870b60ec0a"
        )


@pytest.mark.anyio
async def test_remove_admin_from_model_workspace_admin(users):
    await add_admin_to_model(users["charlie@example.com"], "62b488ba433720870b60ec0a")
    assert await is_admin("62b488ba433720870b60ec0a", users["charlie@example.com"])
    with pytest.raises(BusinessLogicException):
        await remove_user_from_model(
            users["johndoe@example.com"], "62b488ba433720870b60ec0a"
        )


@pytest.mark.anyio
async def test_remove_editor_from_model(users):
    assert await is_editor("62b488ba433720870b60ec0a", users["darwin@example.com"])
    await remove_user_from_model(
        users["darwin@example.com"], "62b488ba433720870b60ec0a"
    )
    assert not await is_editor("62b488ba433720870b60ec0a", users["darwin@example.com"])


@pytest.mark.anyio
async def test_remove_editor_from_model_non_existing_user(not_an_id):
    with pytest.raises(DoesNotExistException):
        await remove_user_from_model(not_an_id, "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_set_name():
    model_id = "62b488ba433720870b60ec0a"
    new_name = "new_name"
    await set_name(model_id, new_name)
    model = await get_model_by_id(model_id)
    assert model.meta.name == new_name


@pytest.mark.anyio
async def test_set_starting_month():
    model_id = "62b488ba433720870b60ec0a"
    new_date = date(2030, 12, 31)
    await set_starting_month(model_id, new_date)
    model = await get_model_by_id(model_id)
    assert model.meta.starting_month == new_date


@pytest.mark.anyio
async def test_set_starting_balance():
    model_id = "62b488ba433720870b60ec0a"
    balance = 1234.56
    await set_starting_balance(model_id, balance)
    model = await get_model_by_id(model_id)
    assert model.meta.starting_balance == balance


@pytest.mark.anyio
async def test_add_model(users, workspaces):
    new_name = "some_new_model"
    workspace = workspaces["ACME Inc."]
    admin = users["johndoe@example.com"]
    r = await create_model(admin, new_name, workspace)
    model = await get_model_by_id(r.inserted_id)
    wsp = await get_workspace(workspace)
    assert model.meta.name == new_name
    assert model.meta.starting_month == date.today()
    assert str(model.meta.workspace) == workspace
    assert admin in [str(x) for x in model.meta.admins]
    assert str(wsp.admin) in [str(x) for x in model.meta.admins]
    assert len(model.sheets) == 2
    assert "Revenues" in [m.meta.name for m in model.sheets]
    assert "Costs" in [m.meta.name for m in model.sheets]


@pytest.mark.anyio
async def test_add_model_no_access(users, workspaces):
    new_name = "some_new_model"
    workspace = workspaces["Boring Co."]
    admin = users["johndoe@example.com"]

    with pytest.raises(NoAccessException):
        await create_model(admin, new_name, workspace)


@pytest.mark.anyio
async def test_add_model_non_existent_user(not_an_id, workspaces):
    new_name = "some_new_model"
    workspace = workspaces["ACME Inc."]

    with pytest.raises(DoesNotExistException):
        await create_model(not_an_id, new_name, workspace)


@pytest.mark.anyio
async def test_add_model_non_existent_workspace(not_an_id, users):
    new_name = "some_new_model"
    admin = users["johndoe@example.com"]

    with pytest.raises(DoesNotExistException):
        await create_model(admin, new_name, not_an_id)


@pytest.mark.anyio
async def test_get_revenues_sheet():
    model_id = "62b488ba433720870b60ec0a"
    sheet_name = "Revenues"
    sheet = await get_revenues_sheet(model_id)
    assert sheet.meta.name == sheet_name


@pytest.mark.anyio
async def test_get_costs_sheet():
    model_id = "62b488ba433720870b60ec0a"
    sheet_name = "Costs"
    sheet = await get_costs_sheet(model_id)
    assert sheet.meta.name == sheet_name


@pytest.mark.anyio
async def test_update_costs_sheet():
    model_id = "62b488ba433720870b60ec0a"
    sheet = await get_costs_sheet(model_id)
    sheet_new = Sheet(**sheet.dict())
    for sec in sheet_new.sections:
        sec.name = sec.name + "_changed"
    await update_costs_sheet(model_id, sheet_new)
    sheet2 = await get_costs_sheet(model_id)
    for sec in sheet2.sections:
        assert sec.name.endswith("_changed")


@pytest.mark.anyio
async def test_update_costs_sheet_cannot_change_meta():
    model_id = "62b488ba433720870b60ec0a"
    sheet = await get_costs_sheet(model_id)
    sheet_new = Sheet(**sheet.dict())
    sheet_new.meta.name = "Revenues"
    await update_costs_sheet(model_id, sheet_new)
    sheet2 = await get_costs_sheet(model_id)
    assert sheet2.meta.name == sheet.meta.name


@pytest.mark.anyio
async def test_update_revenues_sheet():
    model_id = "62b488ba433720870b60ec0a"
    sheet = await get_revenues_sheet(model_id)
    sheet_new = Sheet(**sheet.dict())
    for sec in sheet_new.sections:
        sec.name = sec.name + "_changed"
    await update_revenues_sheet(model_id, sheet_new)
    sheet2 = await get_revenues_sheet(model_id)
    for sec in sheet2.sections:
        assert sec.name.endswith("_changed")


@pytest.mark.anyio
async def test_update_revenues_sheet_cannot_change_meta():
    model_id = "62b488ba433720870b60ec0a"
    sheet = await get_revenues_sheet(model_id)
    sheet_new = Sheet(**sheet.dict())
    sheet_new.meta.name = "Costs"
    await update_revenues_sheet(model_id, sheet_new)
    sheet2 = await get_revenues_sheet(model_id)
    assert sheet2.meta.name == sheet.meta.name


@pytest.mark.anyio
async def test_update_model_employees():
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
    await update_model_employees(model_id, employees)
    model_afterwards = await get_model_by_id(model_id)
    assert length_before == len(model_afterwards.payroll.employees) - 1
    ct = 0
    for e in model_afterwards.payroll.employees:
        if e.name == "Saint West":
            ct += 1
    assert ct == 1


@pytest.mark.anyio
async def test_get_users_of_model(users):
    model_id = "62b488ba433720870b60ec0a"
    all_users = await get_users_for_model(model_id)

    unique = set()
    model = await get_model_by_id(model_id)

    admin_set = set([str(x) for x in model.meta.admins])
    editor_set = set([str(x) for x in model.meta.editors])
    viewer_set = set([str(x) for x in model.meta.viewers])

    usernames = list(admin_set.union(editor_set).union(viewer_set))

    for u in all_users:
        if u.username == "johndoe@example.com":
            assert u.user_role == "Admin"

        if u.user_role == "Admin":
            assert users[u.username] in admin_set
        elif u.user_role == "Editor":
            assert users[u.username] in editor_set
        elif u.user_role == "Viewer":
            assert users[u.username] in viewer_set

        unique.add(u.username)

        assert users[u.username] in usernames

    assert len(all_users) == len(unique)
    assert len(usernames) == len(unique)


@pytest.mark.anyio
async def test_get_users_for_model_model_non_existent():
    with pytest.raises(DoesNotExistException):
        await get_users_for_model("Not a model.")


@pytest.mark.anyio
async def test_demo_model():
    demo_model = await get_demo_model()
    new_model = create_new_demo_model("admin_id_123", "workspace_id_123", demo_model)
    assert new_model.meta.admins == ["admin_id_123"]
    assert new_model.meta.workspace == "workspace_id_123"
