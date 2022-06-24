import pytest

from core.dao.models import (
    has_access_to_model,
    get_model_by_id,
    get_models_for_workspace,
    get_models_for_user,
    is_admin,
    is_editor,
    is_viewer,
    set_admin,
    add_editor_to_model,
    add_viewer_to_model,
    remove_viewer_from_model,
    remove_editor_from_model,
    set_name,
    create_model,
    add_sheet_to_model,
)
from core.dao.users import get_user, user_exists
from core.exceptions import DoesNotExistException, NoAccessException


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
        assert m["meta"]["admin"] == user


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
    await set_admin("charlie@example.com", "62b488ba433720870b60ec0a")
    assert await is_admin("62b488ba433720870b60ec0a", "charlie@example.com")


@pytest.mark.anyio
async def test_set_admin_non_existing_user():
    with pytest.raises(DoesNotExistException):
        await set_admin("not-a-user@example.com", "62b488ba433720870b60ec0a")


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
    assert model["meta"]["name"] == new_name
    assert model["meta"]["workspace"] == workspace
    assert model["meta"]["admin"] == admin


@pytest.mark.anyio
async def test_add_model_no_access():
    new_name = "some_new_model"
    workspace = "Boring Co."
    admin = "johndoe@example.com"

    with pytest.raises(NoAccessException):
        await create_model(admin, new_name, workspace)


@pytest.mark.anyio
async def test_add_sheet():
    model_id = "62b488ba433720870b60ec0a"
    sheet_name = "sheet_name"
    model1 = await get_model_by_id(model_id)
    await add_sheet_to_model(model_id, sheet_name)
    model2 = await get_model_by_id(model_id)
    assert len(model2["data"]) - len(model1["data"]) == 1
    assert sheet_name in [x["meta"]["name"] for x in model2["data"]]
