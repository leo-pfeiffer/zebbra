from fastapi.encoders import jsonable_encoder

from core.dao.database import db
from core.objects import PyObjectId
from core.schemas.integrations import IntegrationProvider, IntegrationAccess
from core.settings import get_settings

settings = get_settings()


async def get_integrationss_for_user(
    user_id: PyObjectId,
) -> list[IntegrationAccess]:
    """
    Get a list of all integration providers that a user has set up.
    :param user_id: the user's id
    :return: list of integration access objects
    """
    integrations = await db.integration_access.find({"user_id": str(user_id)}).to_list(
        length=settings.MAX_MODELS
    )
    return [IntegrationAccess(**obj) for obj in integrations]


async def get_integration_for_user(
    user_id: PyObjectId, integration: IntegrationProvider
) -> IntegrationAccess | None:
    """
    Returns an integration access object for a user and an integration.
    :param user_id: the user's id
    :param integration: the name of the integration
    :return: Integration access object
    """
    res = await db.integration_access.find_one(
        {"user_id": str(user_id), "integration": integration}
    )
    if res is not None:
        return IntegrationAccess(**res)


async def user_has_integration(
    user_id: PyObjectId, integration: IntegrationProvider
) -> bool:
    """
    Returns true if a user has set up an integration with the given provider.
    :param user_id: the user's id
    :param integration: the name of the integration
    :return: True if the integration is set up, false otherwise
    """
    return (
        await db.integration_access.count_documents(
            {"user_id": str(user_id), "integration": integration}
        )
        > 0
    )


async def add_integration_for_user(integration_access: IntegrationAccess):
    """
    Add an integration access object to the database.
    :param integration_access: the new object
    """
    # replace existing integration access
    if await user_has_integration(
        integration_access.user_id, integration_access.integration
    ):
        return db.integration_access.replace_one(
            {
                {
                    "user_id": str(integration_access.user_id),
                    "integration": integration_access.integration,
                }
            },
            jsonable_encoder(integration_access),
        )
    # add new integration access
    else:
        return db.integration_access.insert_one(jsonable_encoder(integration_access))
