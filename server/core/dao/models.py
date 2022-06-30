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
from core.objects import PyObjectId
from core.schemas.models import ModelMeta, UpdateModel, ModelUser
from core.schemas.sheets import Sheet, SheetMeta, Section
from core.settings import get_settings

settings = get_settings()


async def model_exists(model_id: str):
    return await get_model_by_id(model_id) is not None


async def has_access_to_model(model_id: str, user_id: PyObjectId):
    return (
        await db.models.count_documents(
            {
                "_id": model_id,
                "$or": [
                    {"meta.admins": str(user_id)},
                    {"meta.editors": str(user_id)},
                    {"meta.viewers": str(user_id)},
                ],
            }
        )
        > 0
    )


async def is_admin(model_id: str, user_id: PyObjectId):
    model = await db.models.find_one({"_id": model_id})
    return str(user_id) in model["meta"]["admins"]


async def is_editor(model_id: str, user_id: PyObjectId):
    model = await db.models.find_one({"_id": model_id})
    return str(user_id) in model["meta"]["editors"]


async def is_viewer(model_id: str, user_id: PyObjectId):
    model = await db.models.find_one({"_id": model_id})
    return str(user_id) in model["meta"]["viewers"]


async def get_model_by_id(model_id: str):
    return await db.models.find_one({"_id": model_id})


async def get_models_for_workspace(workspace_id: PyObjectId):
    return await db.models.find({"meta.workspace": str(workspace_id)}).to_list(
        length=settings.MAX_MODELS
    )


async def get_models_for_user(user_id: PyObjectId):
    return await db.models.find(
        {
            "$or": [
                {"meta.admins": str(user_id)},
                {"meta.editors": str(user_id)},
                {"meta.viewers": str(user_id)},
            ]
        }
    ).to_list(length=settings.MAX_MODELS)


async def get_admin_models_for_user(user_id: PyObjectId):
    return await db.models.find({"meta.admins": str(user_id)}).to_list(
        length=settings.MAX_MODELS
    )


async def get_users_for_model(model_id: str):
    model = await get_model_by_id(model_id)
    if model is None:
        raise DoesNotExistException("Model does not exist")

    admin_set = set(model["meta"]["admins"])
    editor_set = set(model["meta"]["editors"])
    viewer_set = set(model["meta"]["viewers"])

    user_ids = list(admin_set.union(editor_set).union(viewer_set))
    admins = []
    editors = []
    viewers = []

    def get_user_role(_user_id):
        if _user_id in admin_set:
            return "Admin"
        if _user_id in editor_set:
            return "Editor"
        if _user_id in viewer_set:
            return "Viewer"

    def add_to_list(_user: ModelUser):
        if _user.id in admin_set:
            admins.append(_user)
        if _user.id in editor_set:
            editors.append(_user)
        if _user.id in viewer_set:
            viewers.append(_user)

    for user_id in user_ids:
        user = await get_user(user_id)
        user_role = get_user_role(user_id)
        add_to_list(
            ModelUser(
                _id=str(user.id),
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                user_role=user_role,
            )
        )

    admins.sort(key=lambda x: x.last_name)
    editors.sort(key=lambda x: x.last_name)
    viewers.sort(key=lambda x: x.last_name)
    return admins + editors + viewers


async def add_admin_to_model(user_id: PyObjectId, model_id: str):
    if not await user_exists(user_id):
        raise DoesNotExistException("User does not exist")

    await db.models.update_one(
        {"_id": model_id}, {"$push": {"meta.admins": str(user_id)}}
    )


async def add_editor_to_model(user_id: PyObjectId, model_id: str):
    if not await user_exists(user_id):
        raise DoesNotExistException("User does not exist")

    # don't add as editor if already is editor
    if not await is_editor(model_id, user_id):
        await db.models.update_one(
            {"_id": model_id}, {"$push": {"meta.editors": str(user_id)}}
        )


async def add_viewer_to_model(user_id: PyObjectId, model_id: str):
    if not await user_exists(user_id):
        raise DoesNotExistException("User does not exist")

    # don't add as viewer if already is viewer
    if not await is_viewer(model_id, user_id):
        await db.models.update_one(
            {"_id": model_id}, {"$push": {"meta.viewers": str(user_id)}}
        )


async def remove_admin_from_model(user_id: PyObjectId, model_id: str):
    if not await user_exists(user_id):
        raise DoesNotExistException("User does not exist")

    model = await get_model_by_id(model_id)

    # must have at least one admin
    if len(model["meta"]["admins"]) == 1:
        raise CardinalityConstraintFailedException("Model must have at least one admin")

    # must not remove workspace admin
    workspace = await get_workspace(model["meta"]["workspace"])
    if str(user_id) == str(workspace.admin):
        raise BusinessLogicException("Cannot remove workspace admin from model.")

    await db.models.update_one(
        {"_id": model_id}, {"$pull": {"meta.admins": str(user_id)}}
    )


async def remove_viewer_from_model(user_id: PyObjectId, model_id: str):
    if not await user_exists(user_id):
        raise DoesNotExistException("User does not exist")

    await db.models.update_one(
        {"_id": model_id}, {"$pull": {"meta.viewers": str(user_id)}}
    )


async def remove_editor_from_model(user_id: PyObjectId, model_id: str):
    if not await user_exists(user_id):
        raise DoesNotExistException("User does not exist")
    await db.models.update_one(
        {"_id": model_id}, {"$pull": {"meta.editors": str(user_id)}}
    )


async def set_name(model_id: str, name: str):
    await db.models.update_one({"_id": model_id}, {"$set": {"meta.name": name}})


async def create_model(admin_id: PyObjectId, model_name: str, workspace_id: PyObjectId):
    if not await user_exists(admin_id):
        raise DoesNotExistException("User does not exist")

    wsp = await get_workspace(workspace_id)

    if wsp is None:
        raise DoesNotExistException("Workspace does not exist")

    if not await is_user_in_workspace(admin_id, workspace_id):
        raise NoAccessException("User has no access to workspace.")

    admins = [admin_id]
    if admin_id != wsp.admin:
        admins.append(wsp.admin)

    meta = ModelMeta(
        **{
            "name": model_name,
            "admins": admins,
            "workspace": workspace_id,
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
