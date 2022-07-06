from fastapi.encoders import jsonable_encoder

from core.dao.database import db
from core.schemas.integrations import IntegrationProvider, IntegrationAccess
from core.settings import get_settings

settings = get_settings()


async def get_integrations_for_workspace(
    workspace_id: str,
) -> list[IntegrationAccess]:
    """
    Get a list of all integration providers that have been set up for a workspace
    :param workspace_id: the id of the workspace
    :return: list of integration access objects
    """
    integrations = await db.integration_access.find(
        {"workspace_id": workspace_id}
    ).to_list(length=settings.MAX_MODELS)
    return [IntegrationAccess(**obj) for obj in integrations]


async def get_integration_for_workspace(
    workspace_id: str, integration: IntegrationProvider
) -> IntegrationAccess | None:
    """
    Returns an integration access object for a workspace and an integration
    :param workspace_id: the id of the workspace
    :param integration: the name of the integration
    :return: Integration access object
    """
    res = await db.integration_access.find_one(
        {"workspace_id": workspace_id, "integration": integration}
    )
    if res is not None:
        return IntegrationAccess(**res)


async def workspace_has_integration(
    workspace_id: str, integration: IntegrationProvider
) -> bool:
    """
    Returns true if a workspace has set up an integration with the given provider
    :param workspace_id: the user's id
    :param integration: the name of the integration
    :return: True if the integration is set up, false otherwise
    """
    return (
        await db.integration_access.count_documents(
            {"workspace_id": workspace_id, "integration": integration}
        )
        > 0
    )


async def add_integration_for_workspace(integration_access: IntegrationAccess):
    """
    Add an integration access object to the database
    :param integration_access: the new object
    """
    # replace existing integration access
    if await workspace_has_integration(
        integration_access.workspace_id, integration_access.integration
    ):
        return db.integration_access.replace_one(
            {
                "workspace_id": integration_access.workspace_id,
                "integration": integration_access.integration,
            },
            {**integration_access.dict()},
        )
    # add new integration access
    else:
        return db.integration_access.insert_one(jsonable_encoder(integration_access))


async def set_requires_reconnect(
    workspace_id: str, integration: IntegrationProvider, requires_reconnect: bool
):
    """
    Set the requires_reconnect field of the integration access data
    :param workspace_id: ID of the workspace
    :param integration: Name of the integration
    :param requires_reconnect: True / False
    """
    return await db.integration_access.update_one(
        {"workspace_id": workspace_id, "integration": integration},
        {"$set": {"requires_reconnect": requires_reconnect}},
    )
