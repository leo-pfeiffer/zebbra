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
    remove_viewer_from_model,
    remove_editor_from_model,
    set_name,
    create_model,
    update_sheet_meta_in_model,
    update_sheet_sections_in_model,
    get_sheet_by_name,
    remove_admin_from_model,
    get_users_for_model,
)
from core.dao.workspaces import get_workspace
from core.exceptions import (
    DoesNotExistException,
    NoAccessException,
    UniqueConstraintFailedException,
    BusinessLogicException,
    CardinalityConstraintFailedException,
)
from core.schemas.sheets import SheetMeta, Section


@pytest.mark.anyio
async def test_has_access_to_model_admin():
    assert await has_access_to_model("62b488ba433720870b60ec0a", "johndoe@example.com")


@pytest.mark.anyio
async def test_has_access_to_model_editor():
    assert await has_access_to_model("62b488ba433720870b60ec0a", "darwin@example.com")


@pytest.mark.anyio
async def test_has_access_to_model_viewer():
    assert await has_access_to_model("62b488ba433720870b60ec0a", "charlie@example.com")


@pytest.mark.anyio
async def test_has_access_to_model_false():
    assert not await has_access_to_model("62b488ba433720870b60ec0a", "bob@example.com")


@pytest.mark.anyio
async def test_get_model_by_id():
    model_id = "62b488ba433720870b60ec0a"
    models = await get_model_by_id(model_id)
    assert models["_id"] == model_id


@pytest.mark.anyio
async def test_get_model_by_id_no_results():
    model_id = "not_an_id"
    assert await get_model_by_id(model_id) is None


@pytest.mark.anyio
async def test_get_models_for_workspace():
    wsp = "ACME Inc."
    models = await get_models_for_workspace(wsp)
    assert len(models) == 1
    for m in models:
        assert m["meta"]["workspace"] == wsp


@pytest.mark.anyio
async def test_get_models_for_workspace_no_results():
    wsp = "Not a workspace"
    models = await get_models_for_workspace(wsp)
    assert len(models) == 0


@pytest.mark.anyio
async def test_get_models_for_user_admin():
    user = "johndoe@example.com"
    models = await get_models_for_user(user)
    assert len(models) == 1
    for m in models:
        assert user in m["meta"]["admins"]


@pytest.mark.anyio
async def test_get_models_for_user_editor():
    user = "darwin@example.com"
    models = await get_models_for_user(user)
    assert len(models) == 1
    for m in models:
        assert user in m["meta"]["editors"]


@pytest.mark.anyio
async def test_get_models_for_user_viewer():
    user = "charlie@example.com"
    models = await get_models_for_user(user)
    assert len(models) == 1
    for m in models:
        assert user in m["meta"]["viewers"]


@pytest.mark.anyio
async def test_get_models_for_user_no_results():
    user = "not-a-user@example.com"
    models = await get_models_for_user(user)
    assert len(models) == 0


@pytest.mark.anyio
async def test_is_admin_true():
    assert await is_admin("62b488ba433720870b60ec0a", "johndoe@example.com")


@pytest.mark.anyio
async def test_is_admin_false():
    assert not await is_admin("62b488ba433720870b60ec0a", "darwin@example.com")


@pytest.mark.anyio
async def test_is_editor_true():
    assert await is_editor("62b488ba433720870b60ec0a", "darwin@example.com")


@pytest.mark.anyio
async def test_is_editor_false():
    assert not await is_editor("62b488ba433720870b60ec0a", "charlie@example.com")


@pytest.mark.anyio
async def test_is_viewer_true():
    assert await is_viewer("62b488ba433720870b60ec0a", "charlie@example.com")


@pytest.mark.anyio
async def test_is_viewer_false():
    assert not await is_viewer("62b488ba433720870b60ec0a", "darwing@example.com")


@pytest.mark.anyio
async def test_set_admin():
    assert await is_admin("62b488ba433720870b60ec0a", "johndoe@example.com")
    await add_admin_to_model("charlie@example.com", "62b488ba433720870b60ec0a")
    assert await is_admin("62b488ba433720870b60ec0a", "charlie@example.com")


@pytest.mark.anyio
async def test_set_admin_non_existing_user():
    with pytest.raises(DoesNotExistException):
        await add_admin_to_model("not-a-user@example.com", "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_add_editor_to_model():
    assert not await is_editor("62b488ba433720870b60ec0a", "johndoe@example.com")
    await add_editor_to_model("darwin@example.com", "62b488ba433720870b60ec0a")
    assert await is_editor("62b488ba433720870b60ec0a", "darwin@example.com")


@pytest.mark.anyio
async def test_add_editor_to_model_non_existing_user():
    with pytest.raises(DoesNotExistException):
        await add_editor_to_model("not-a-user@example.com", "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_add_viewer_to_model():
    assert not await is_viewer("62b488ba433720870b60ec0a", "darwin@example.com")
    await add_viewer_to_model("darwin@example.com", "62b488ba433720870b60ec0a")
    assert await is_viewer("62b488ba433720870b60ec0a", "charlie@example.com")


@pytest.mark.anyio
async def test_add_viewer_to_model_non_existing_user():
    with pytest.raises(DoesNotExistException):
        await add_viewer_to_model("not-a-user@example.com", "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_remove_viewer_from_model():
    assert await is_viewer("62b488ba433720870b60ec0a", "charlie@example.com")
    await remove_viewer_from_model("charlie@example.com", "62b488ba433720870b60ec0a")
    assert not await is_viewer("62b488ba433720870b60ec0a", "charlie@example.com")


@pytest.mark.anyio
async def test_remove_viewer_from_model_non_existing_user():
    with pytest.raises(DoesNotExistException):
        await remove_viewer_from_model(
            "not-a-user@example.com", "62b488ba433720870b60ec0a"
        )


@pytest.mark.anyio
async def test_remove_admin_from_model():
    await add_admin_to_model("charlie@example.com", "62b488ba433720870b60ec0a")
    assert await is_admin("62b488ba433720870b60ec0a", "charlie@example.com")
    await remove_admin_from_model("charlie@example.com", "62b488ba433720870b60ec0a")
    assert not await is_admin("62b488ba433720870b60ec0a", "charlie@example.com")


@pytest.mark.anyio
async def test_remove_admin_from_model_non_existing_user():
    with pytest.raises(DoesNotExistException):
        await remove_admin_from_model(
            "not-a-user@example.com", "62b488ba433720870b60ec0a"
        )


@pytest.mark.anyio
async def test_remove_admin_from_model_only_one_admin():
    with pytest.raises(CardinalityConstraintFailedException):
        await remove_admin_from_model("johndoe@example.com", "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_remove_admin_from_model_workspace_admin():
    await add_admin_to_model("charlie@example.com", "62b488ba433720870b60ec0a")
    assert await is_admin("62b488ba433720870b60ec0a", "charlie@example.com")
    with pytest.raises(BusinessLogicException):
        await remove_admin_from_model("johndoe@example.com", "62b488ba433720870b60ec0a")


@pytest.mark.anyio
async def test_remove_editor_from_model():
    assert await is_editor("62b488ba433720870b60ec0a", "darwin@example.com")
    await remove_editor_from_model("darwin@example.com", "62b488ba433720870b60ec0a")
    assert not await is_editor("62b488ba433720870b60ec0a", "darwin@example.com")


@pytest.mark.anyio
async def test_remove_editor_from_model_non_existing_user():
    with pytest.raises(DoesNotExistException):
        await remove_editor_from_model(
            "not-a-user@example.com", "62b488ba433720870b60ec0a"
        )


@pytest.mark.anyio
async def test_set_name():
    model_id = "62b488ba433720870b60ec0a"
    new_name = "new_name"
    await set_name(model_id, new_name)
    model = await get_model_by_id(model_id)
    assert model["meta"]["name"] == new_name


@pytest.mark.anyio
async def test_add_model():
    new_name = "some_new_model"
    workspace = "ACME Inc."
    admin = "johndoe@example.com"
    r = await create_model(admin, new_name, workspace)
    model = await get_model_by_id(r.inserted_id)
    wsp = await get_workspace(workspace)
    assert model["meta"]["name"] == new_name
    assert model["meta"]["workspace"] == workspace
    assert admin in model["meta"]["admins"]
    assert wsp.admin in model["meta"]["admins"]


@pytest.mark.anyio
async def test_add_model_no_access():
    new_name = "some_new_model"
    workspace = "Boring Co."
    admin = "johndoe@example.com"

    with pytest.raises(NoAccessException):
        await create_model(admin, new_name, workspace)


@pytest.mark.anyio
async def test_add_model_non_existent_user():
    new_name = "some_new_model"
    workspace = "ACME Inc."
    admin = "not-a-user@example.com"

    with pytest.raises(DoesNotExistException):
        await create_model(admin, new_name, workspace)


@pytest.mark.anyio
async def test_add_model_non_existent_workspace():
    new_name = "some_new_model"
    workspace = "Not a workspace"
    admin = "johndoe@example.com"

    with pytest.raises(DoesNotExistException):
        await create_model(admin, new_name, workspace)


@pytest.mark.anyio
async def test_get_sheet_by_name():
    model_id = "62b488ba433720870b60ec0a"
    sheet_name = "sheet1"
    sheet = await get_sheet_by_name(model_id, sheet_name)
    assert sheet.meta.name == sheet_name


@pytest.mark.anyio
async def test_get_sheet_by_name_non_existent():
    model_id = "62b488ba433720870b60ec0a"
    sheet_name = "not a sheet"
    assert await get_sheet_by_name(model_id, sheet_name) is None


@pytest.mark.anyio
async def test_update_sheet_meta():
    model_id = "62b488ba433720870b60ec0a"
    model1 = await get_model_by_id(model_id)
    old_sheet_name = model1["sheets"][0]["meta"]["name"]
    new_sheet_name = "new sheet name"
    new_meta = SheetMeta(name=new_sheet_name)

    await update_sheet_meta_in_model(model_id, old_sheet_name, new_meta)

    model1 = await get_model_by_id(model_id)
    assert model1["sheets"][0]["meta"]["name"] == new_sheet_name


@pytest.mark.anyio
async def test_update_sheet_meta_duplicate_name():
    model_id = "62b488ba433720870b60ec0a"
    model1 = await get_model_by_id(model_id)
    old_sheet_name = model1["sheets"][0]["meta"]["name"]
    new_meta = SheetMeta(name=old_sheet_name)

    with pytest.raises(UniqueConstraintFailedException):
        await update_sheet_meta_in_model(model_id, old_sheet_name, new_meta)


@pytest.mark.anyio
async def test_update_sheet_data():
    model_id = "62b488ba433720870b60ec0a"
    model1 = await get_model_by_id(model_id)
    old_sheet_name = model1["sheets"][0]["meta"]["name"]

    new_data = [
        Section(**{"name": "section1", "rows": [], "end_row": None}),
        Section(**{"name": "section2", "rows": [], "end_row": None}),
    ]

    await update_sheet_sections_in_model(model_id, old_sheet_name, new_data)

    model2 = await get_model_by_id(model_id)
    assert len(model2["sheets"][0]["sections"]) == 2
    assert model2["sheets"][0]["sections"][0]["name"] == "section1"
    assert model2["sheets"][0]["sections"][1]["name"] == "section2"


@pytest.mark.anyio
async def test_get_users_of_model(access_token):
    model_id = "62b488ba433720870b60ec0a"
    users = await get_users_for_model(model_id)

    unique = set()
    model = await get_model_by_id(model_id)

    admin_set = set(model["meta"]["admins"])
    editor_set = set(model["meta"]["editors"])
    viewer_set = set(model["meta"]["viewers"])

    usernames = list(admin_set.union(editor_set).union(viewer_set))

    for u in users:
        if u.username == "johndoe@example.com":
            assert u.user_role == "Admin"

        if u.user_role == "Admin":
            assert u.username in admin_set
        elif u.user_role == "Editor":
            assert u.username in editor_set
        elif u.user_role == "Viewer":
            assert u.username in viewer_set

        unique.add(u.username)

        assert u.username in usernames

    assert len(users) == len(unique)
    assert len(usernames) == len(unique)


@pytest.mark.anyio
async def test_get_users_for_model_model_non_existent(access_token):
    with pytest.raises(DoesNotExistException):
        await get_users_for_model("Not a model.")
