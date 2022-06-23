from core.dao.database import db
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
