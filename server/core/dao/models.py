from fastapi.encoders import jsonable_encoder

from core.dao.database import db
from core.dao.users import user_exists
from core.dao.workspaces import is_user_in_workspace
from core.exceptions import (
    DoesNotExistException,
    NoAccessException,
    UniqueConstraintFailedException,
)
from core.schemas.models import ModelMeta, UpdateModel
from core.schemas.sheets import Sheet, SheetMeta, Section
from core.settings import get_settings

settings = get_settings()


async def model_exists(id: str):
    return await get_model_by_id(id) is not None


async def has_access_to_model(id: str, username: str):
    return (
        await db.models.count_documents(
            {
                "_id": id,
                "$or": [
                    {"meta.admin": username},
                    {"meta.editors": username},
                    {"meta.viewers": username},
                ],
            }
        )
        > 0
    )


async def is_admin(id: str, username: str):
    model = await db.models.find_one({"_id": id})
    return model["meta"]["admin"] == username


async def is_editor(id: str, username: str):
    model = await db.models.find_one({"_id": id})
    return username in model["meta"]["editors"]


async def is_viewer(id: str, username: str):
    model = await db.models.find_one({"_id": id})
    return username in model["meta"]["viewers"]


async def get_model_by_id(id: str):
    return await db.models.find_one({"_id": id})


async def get_models_for_workspace(workspace: str):
    return await db.models.find({"meta.workspace": workspace}).to_list(
        length=settings.MAX_MODELS
    )


async def get_models_for_user(username: str):
    return await db.models.find(
        {
            "$or": [
                {"meta.admin": username},
                {"meta.editors": username},
                {"meta.viewers": username},
            ]
        }
    ).to_list(length=settings.MAX_MODELS)


async def set_admin(username: str, model_id: str):
    if not await user_exists(username):
        raise DoesNotExistException("User does not exist")

    await db.models.update_one({"_id": model_id}, {"$set": {"meta.admin": username}})


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

    if not await is_user_in_workspace(admin, workspace):
        raise NoAccessException("User has no access to workspace.")

    meta = ModelMeta(
        **{
            "name": model_name,
            "admin": admin,
            "workspace": workspace,
            "editors": [],
            "viewers": [],
        }
    )
    model = UpdateModel(**{"meta": meta, "data": []})
    return await db.models.insert_one(jsonable_encoder(model))


async def add_sheet_to_model(model_id: str, sheet_name: str):

    # sheet names must be unique within model
    if (
        await db.models.count_documents({"_id": model_id, "data.meta.name": sheet_name})
        > 0
    ):
        raise UniqueConstraintFailedException("Sheet names must be unique within model")

    sheet = Sheet(**{"meta": SheetMeta(name=sheet_name), "data": []})

    return await db.models.update_one(
        {"_id": model_id}, {"$push": {"data": jsonable_encoder(sheet)}}
    )


async def delete_sheet_from_model(model_id: str, sheet_name: str):
    return await db.models.update_one(
        {"_id": model_id}, {"$pull": {"data": {"meta.name": sheet_name}}}
    )


async def update_sheet_meta_in_model(
    model_id: str, sheet_name: str, new_meta: SheetMeta
):
    # sheet names must be unique within model
    if (
        await db.models.count_documents(
            {"_id": model_id, "data.meta.name": new_meta.name}
        )
        > 0
    ):
        raise UniqueConstraintFailedException("Sheet names must be unique within model")

    return await db.models.update_one(
        {"_id": model_id, "data.meta.name": sheet_name},
        {"$set": {"data.$.meta": jsonable_encoder(new_meta)}},
    )


async def update_sheet_data_in_model(
    model_id: str, sheet_name: str, new_data: list[Section]
):
    return await db.models.update_one(
        {"_id": model_id, "data.meta.name": sheet_name},
        {"$set": {"data.$.data": jsonable_encoder(new_data)}},
    )
