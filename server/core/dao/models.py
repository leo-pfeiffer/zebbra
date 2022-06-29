from fastapi.encoders import jsonable_encoder

from core.dao.database import db
from core.dao.users import user_exists, get_user
from core.dao.workspaces import is_user_in_workspace, get_workspace
from core.exceptions import (
    DoesNotExistException,
    NoAccessException,
    UniqueConstraintFailedException,
    CardinalityConstraintFailedException,
    BusinessLogicException,
)
from core.schemas.models import ModelMeta, UpdateModel, ModelUser
from core.schemas.sheets import Sheet, SheetMeta, Section
from core.settings import get_settings

settings = get_settings()


async def model_exists(model_id: str):
    return await get_model_by_id(model_id) is not None


async def has_access_to_model(model_id: str, username: str):
    return (
        await db.models.count_documents(
            {
                "_id": model_id,
                "$or": [
                    {"meta.admins": username},
                    {"meta.editors": username},
                    {"meta.viewers": username},
                ],
            }
        )
        > 0
    )


async def is_admin(model_id: str, username: str):
    model = await db.models.find_one({"_id": model_id})
    return username in model["meta"]["admins"]


async def is_editor(model_id: str, username: str):
    model = await db.models.find_one({"_id": model_id})
    return username in model["meta"]["editors"]


async def is_viewer(model_id: str, username: str):
    model = await db.models.find_one({"_id": model_id})
    return username in model["meta"]["viewers"]


async def get_model_by_id(model_id: str):
    return await db.models.find_one({"_id": model_id})


async def get_models_for_workspace(workspace: str):
    return await db.models.find({"meta.workspace": workspace}).to_list(
        length=settings.MAX_MODELS
    )


async def get_models_for_user(username: str):
    return await db.models.find(
        {
            "$or": [
                {"meta.admins": username},
                {"meta.editors": username},
                {"meta.viewers": username},
            ]
        }
    ).to_list(length=settings.MAX_MODELS)


async def get_admin_models_for_user(username: str):
    return await db.models.find({"meta.admins": username}).to_list(
        length=settings.MAX_MODELS
    )


async def get_users_for_model(model_id: str):
    model = await get_model_by_id(model_id)
    if model is None:
        raise DoesNotExistException("Model does not exist")

    admin_set = set(model["meta"]["admins"])
    editor_set = set(model["meta"]["editors"])
    viewer_set = set(model["meta"]["viewers"])

    usernames = list(admin_set.union(editor_set).union(viewer_set))
    admins = []
    editors = []
    viewers = []

    def get_user_role(_username):
        if _username in admin_set:
            return "Admin"
        if _username in editor_set:
            return "Editor"
        if _username in viewer_set:
            return "Viewer"

    def add_to_list(_user: ModelUser):
        if _user.username in admin_set:
            admins.append(_user)
        if _user.username in editor_set:
            editors.append(_user)
        if _user.username in viewer_set:
            viewers.append(_user)

    for username in usernames:
        user = await get_user(username)
        user_role = get_user_role(user.username)
        add_to_list(
            ModelUser(
                username=username,
                first_name=user.first_name,
                last_name=user.last_name,
                user_role=user_role,
            )
        )

    admins.sort(key=lambda x: x.last_name)
    editors.sort(key=lambda x: x.last_name)
    viewers.sort(key=lambda x: x.last_name)
    return admins + editors + viewers


async def add_admin_to_model(username: str, model_id: str):
    if not await user_exists(username):
        raise DoesNotExistException("User does not exist")

    await db.models.update_one({"_id": model_id}, {"$push": {"meta.admins": username}})


async def add_editor_to_model(username: str, model_id: str):
    if not await user_exists(username):
        raise DoesNotExistException("User does not exist")

    # don't add as editor if already is editor
    if not await is_editor(model_id, username):
        await db.models.update_one(
            {"_id": model_id}, {"$push": {"meta.editors": username}}
        )


async def add_viewer_to_model(username: str, model_id: str):
    if not await user_exists(username):
        raise DoesNotExistException("User does not exist")

    # don't add as viewer if already is viewer
    if not await is_viewer(model_id, username):
        await db.models.update_one(
            {"_id": model_id}, {"$push": {"meta.viewers": username}}
        )


async def remove_admin_from_model(username: str, model_id: str):
    if not await user_exists(username):
        raise DoesNotExistException("User does not exist")

    model = await get_model_by_id(model_id)

    # must have at least one admin
    if len(model["meta"]["admins"]) == 1:
        raise CardinalityConstraintFailedException("Model must have at least one admin")

    # must not remove workspace admin
    workspace = await get_workspace(model["meta"]["workspace"])
    if username == workspace.admin:
        raise BusinessLogicException("Cannot remove workspace admin from model.")

    await db.models.update_one({"_id": model_id}, {"$pull": {"meta.admins": username}})


async def remove_viewer_from_model(username: str, model_id: str):
    if not await user_exists(username):
        raise DoesNotExistException("User does not exist")

    await db.models.update_one({"_id": model_id}, {"$pull": {"meta.viewers": username}})


async def remove_editor_from_model(username: str, model_id: str):
    if not await user_exists(username):
        raise DoesNotExistException("User does not exist")
    await db.models.update_one({"_id": model_id}, {"$pull": {"meta.editors": username}})


async def set_name(model_id: str, name: str):
    await db.models.update_one({"_id": model_id}, {"$set": {"meta.name": name}})


async def create_model(admin: str, model_name: str, workspace: str):
    if not await user_exists(admin):
        raise DoesNotExistException("User does not exist")

    wsp = await get_workspace(workspace)

    if wsp is None:
        raise DoesNotExistException("Workspace does not exist")

    if not await is_user_in_workspace(admin, workspace):
        raise NoAccessException("User has no access to workspace.")

    admins = [admin]
    if admin != wsp.admin:
        admins.append(wsp.admin)

    meta = ModelMeta(
        **{
            "name": model_name,
            "admins": admins,
            "workspace": workspace,
            "editors": [],
            "viewers": [],
        }
    )
    model = UpdateModel(**{"meta": meta, "sheets": []})
    return await db.models.insert_one(jsonable_encoder(model))


async def update_sheet_meta_in_model(
    model_id: str, sheet_name: str, new_meta: SheetMeta
):
    # sheet names must be unique within model
    if (
        await db.models.count_documents(
            {"_id": model_id, "sheets.meta.name": new_meta.name}
        )
        > 0
    ):
        raise UniqueConstraintFailedException("Sheet names must be unique within model")

    return await db.models.update_one(
        {"_id": model_id, "sheets.meta.name": sheet_name},
        {"$set": {"sheets.$.meta": jsonable_encoder(new_meta)}},
    )


async def update_sheet_sections_in_model(
    model_id: str, sheet_name: str, new_sections: list[Section]
):
    return await db.models.update_one(
        {"_id": model_id, "sheets.meta.name": sheet_name},
        {"$set": {"sheets.$.sections": jsonable_encoder(new_sections)}},
    )


async def get_sheet_by_name(model_id: str, sheet_name: str) -> Sheet:
    model = await db.models.find_one(
        {"_id": model_id, "sheets.meta.name": sheet_name},
    )

    if model is not None:
        for sheet in model["sheets"]:
            if sheet["meta"]["name"] == sheet_name:
                return Sheet(**sheet)
