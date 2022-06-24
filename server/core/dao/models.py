from core.dao.database import db
from core.dao.users import user_exists
from core.exceptions import DoesNotExistException
from core.settings import get_settings

settings = get_settings()


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
