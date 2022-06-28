import pytest

from core.dao.models import get_models_for_user, get_models_for_workspace
from core.exceptions import UniqueConstraintFailedException, BusinessLogicException
from core.dao.users import (
    get_user,
    delete_user_full,
    add_user_to_workspace,
    create_user,
    set_user_otp_secret,
    set_user_otp_secret_validated,
    update_username,
    update_user_field,
    remove_user_from_workspace,
)
from core.dao.workspaces import get_workspaces_of_user, create_workspace, get_workspace
from core.schemas.users import UserInDB


@pytest.mark.anyio
async def test_create_user():
    new_user = UserInDB(
        **{
            "username": "another@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "workspaces": ["ACME Inc."],
            "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
            "disabled": False,
        }
    )
    await create_user(new_user)
    user = await get_user("another@example.com")
    assert user is not None


@pytest.mark.anyio
async def test_cannot_create_user_with_duplicate_username():
    new_user = UserInDB(
        **{
            "username": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "workspaces": ["ACME Inc."],
            "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
            "disabled": False,
        }
    )
    with pytest.raises(UniqueConstraintFailedException):
        await create_user(new_user)


@pytest.mark.anyio
async def test_get_user_returns_user():
    user = await get_user("johndoe@example.com")
    assert user.username == "johndoe@example.com"


@pytest.mark.anyio
async def test_get_non_existing_user_returns_none():
    user = await get_user("notauser@me.com")
    assert user is None


@pytest.mark.anyio
async def test_delete_user_deletes_user():
    await delete_user_full("johndoe@example.com")
    assert await get_user("johndoe@example.com") is None


@pytest.mark.anyio
async def test_delete_user_deletes_workspace_membership():
    assert len(await get_workspaces_of_user("johndoe@example.com")) == 1
    await delete_user_full("johndoe@example.com")
    assert len(await get_workspaces_of_user("johndoe@example.com")) == 0


@pytest.mark.anyio
async def test_add_user_to_workspace():
    wsp = "Boring Co."
    username = "johndoe@example.com"
    workspace_before = await get_workspace(wsp)
    await add_user_to_workspace(username, wsp)
    user = await get_user(username)
    assert len(user.workspaces) == 2
    assert wsp in user.workspaces
    workspace_after = await get_workspace(wsp)
    assert len(workspace_after.users) - len(workspace_before.users) == 1
    assert username in workspace_after.users


@pytest.mark.anyio
async def test_set_otp_secret():
    username = "johndoe@example.com"
    secret = "the secret"
    await set_user_otp_secret(username, secret)
    user = await get_user(username)
    assert user.otp_secret == secret


@pytest.mark.anyio
async def test_set_otp_secret_sets_validated_false():
    username = "johndoe@example.com"
    secret = "the secret"
    await set_user_otp_secret_validated(username)
    await set_user_otp_secret(username, secret)
    user = await get_user(username)
    assert not user.otp_validated


@pytest.mark.anyio
async def test_set_otp_validated():
    username = "johndoe@example.com"
    await set_user_otp_secret_validated(username)
    user = await get_user(username)
    assert user.otp_validated


@pytest.mark.anyio
async def test_update_username():
    username = "johndoe@example.com"
    new_username = "nolongerjohn@example.com"
    await update_username(username, new_username)

    assert await get_user(new_username) is not None
    assert await get_user(username) is None

    assert len(await get_workspaces_of_user(username)) == 0
    assert len(await get_models_for_user(username)) == 0


@pytest.mark.anyio
async def test_update_username_duplicate():
    username = "johndoe@example.com"
    new_username = "johndoe@example.com"

    with pytest.raises(UniqueConstraintFailedException):
        await update_username(username, new_username)


@pytest.mark.anyio
async def test_update_first_name():
    username = "johndoe@example.com"
    first_name = "Alfred"
    await update_user_field(username, "first_name", first_name)

    user = await get_user(username)
    assert user.first_name == first_name


@pytest.mark.anyio
async def test_update_last_name():
    username = "johndoe@example.com"
    value = "Hitchcock"
    await update_user_field(username, "last_name", value)

    user = await get_user(username)
    assert user.last_name == value


@pytest.mark.anyio
async def test_update_password():
    username = "johndoe@example.com"
    value = "secret"
    await update_user_field(username, "hashed_password", value)

    user = await get_user(username)
    assert user.hashed_password == value


@pytest.mark.anyio
async def test_update_non_existent_field():
    username = "johndoe@example.com"
    value = "secret"
    with pytest.raises(ValueError):
        await update_user_field(username, "some_random_field", value)


@pytest.mark.anyio
async def test_remove_user_from_workspace():
    u = "charlie@example.com"
    w = "ACME Inc."
    await remove_user_from_workspace(u, w)
    wsp = await get_workspace("ACME Inc.")
    assert u not in wsp.users
    charlie = await get_user(u)
    assert w not in charlie.workspaces


@pytest.mark.anyio
async def test_remove_user_from_workspace_cannot_remove_admin():
    u = "johndoe@example.com"
    w = "ACME Inc."
    with pytest.raises(BusinessLogicException):
        await remove_user_from_workspace(u, w)


@pytest.mark.anyio
async def test_remove_user_from_workspace_remove_from_models():
    u = "charlie@example.com"
    w = "ACME Inc."
    await remove_user_from_workspace(u, w)
    models = await get_models_for_workspace("ACME Inc.")
    for m in models:
        assert u not in m["meta"]["admins"]
        assert u not in m["meta"]["editors"]
        assert u not in m["meta"]["viewers"]
