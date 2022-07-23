import pytest

from core.dao.models import get_models_for_workspace
from core.exceptions import UniqueConstraintFailedException, BusinessLogicException
from core.dao.users import (
    get_user,
    delete_user_full,
    create_user,
    set_user_otp_secret,
    set_user_otp_secret_validated,
    update_username,
    update_user_field,
    remove_user_from_workspace,
    get_user_by_username,
)
from core.dao.workspaces import (
    get_workspaces_of_user,
    get_workspace,
)
from core.schemas.users import UserInDB


@pytest.mark.anyio
async def test_create_user():
    new_user = UserInDB(
        **{
            "username": "another@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
            "disabled": False,
        }
    )
    await create_user(new_user)
    user = await get_user_by_username("another@example.com")
    assert user is not None


@pytest.mark.anyio
async def test_cannot_create_user_with_duplicate_username():
    new_user = UserInDB(
        **{
            "username": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "hashed_password": "$2b$12$JObcoGR6lNWg3ztKdhEK/OtPjUoltMlHJIg99ctXPaBCNQH1EMts.",
            "disabled": False,
        }
    )
    with pytest.raises(UniqueConstraintFailedException):
        await create_user(new_user)


@pytest.mark.anyio
async def test_get_user_returns_user(users):
    user = await get_user(users["johndoe@example.com"])
    assert user.username == "johndoe@example.com"


@pytest.mark.anyio
async def test_get_non_existing_user_returns_none(not_an_id):
    user = await get_user(not_an_id)
    assert user is None


@pytest.mark.anyio
async def test_delete_user_deletes_user(users):
    await delete_user_full(users["johndoe@example.com"])
    assert await get_user(users["johndoe@example.com"]) is None


@pytest.mark.anyio
async def test_delete_user_deletes_workspace_membership(users):
    assert len(await get_workspaces_of_user(users["johndoe@example.com"])) == 1
    await delete_user_full(users["johndoe@example.com"])
    assert len(await get_workspaces_of_user(users["johndoe@example.com"])) == 0


@pytest.mark.anyio
async def test_set_otp_secret(users):
    u = users["johndoe@example.com"]
    secret = "the secret"
    await set_user_otp_secret(u, secret)
    user = await get_user(u)
    assert user.otp_secret == secret


@pytest.mark.anyio
async def test_set_otp_secret_sets_validated_false(users):
    u = users["johndoe@example.com"]
    secret = "the secret"
    await set_user_otp_secret_validated(u)
    await set_user_otp_secret(u, secret)
    user = await get_user(u)
    assert not user.otp_validated


@pytest.mark.anyio
async def test_set_otp_validated(users):
    u = users["johndoe@example.com"]
    await set_user_otp_secret_validated(u)
    user = await get_user(u)
    assert user.otp_validated


@pytest.mark.anyio
async def test_update_username(users):
    user_id = users["johndoe@example.com"]
    new_username = "nolongerjohn@example.com"
    await update_username(user_id, new_username)

    assert await get_user_by_username(new_username) is not None
    assert await get_user_by_username("johndoe@example.com") is None


@pytest.mark.anyio
async def test_update_username_duplicate(users):
    user_id = users["johndoe@example.com"]
    new_username = "johndoe@example.com"

    with pytest.raises(UniqueConstraintFailedException):
        await update_username(user_id, new_username)


@pytest.mark.anyio
async def test_update_first_name(users):
    user_id = users["johndoe@example.com"]
    first_name = "Alfred"
    await update_user_field(user_id, "first_name", first_name)

    user = await get_user(user_id)
    assert user.first_name == first_name


@pytest.mark.anyio
async def test_update_last_name(users):
    user_id = users["johndoe@example.com"]
    value = "Hitchcock"
    await update_user_field(user_id, "last_name", value)

    user = await get_user(user_id)
    assert user.last_name == value


@pytest.mark.anyio
async def test_update_password(users):
    user_id = users["johndoe@example.com"]
    value = "secret"
    await update_user_field(user_id, "hashed_password", value)

    user = await get_user(user_id)
    assert user.hashed_password == value


@pytest.mark.anyio
async def test_update_non_existent_field(users):
    user_id = users["johndoe@example.com"]
    value = "secret"
    with pytest.raises(ValueError):
        await update_user_field(user_id, "some_random_field", value)


@pytest.mark.anyio
async def test_remove_user_from_workspace(users, workspaces):
    u = users["charlie@example.com"]
    w = workspaces["ACME Inc."]
    await remove_user_from_workspace(u, w)
    wsp = await get_workspace(w)
    assert u not in wsp.users


@pytest.mark.anyio
async def test_remove_user_from_workspace_cannot_remove_admin(users, workspaces):
    u = users["johndoe@example.com"]
    w = workspaces["ACME Inc."]
    with pytest.raises(BusinessLogicException):
        await remove_user_from_workspace(u, w)


@pytest.mark.anyio
async def test_remove_user_from_workspace_remove_from_models(users, workspaces):
    u = users["charlie@example.com"]
    w = workspaces["ACME Inc."]
    await remove_user_from_workspace(u, w)
    models = await get_models_for_workspace(w)
    for m in models:
        assert u not in [str(x) for x in m.meta.admins]
        assert u not in [str(x) for x in m.meta.editors]
        assert u not in [str(x) for x in m.meta.viewers]
