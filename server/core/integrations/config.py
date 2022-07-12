from typing import get_args, Callable

from fastapi import FastAPI
from core.integrations.adapters.adapter import FetchAdapter
from core.integrations.adapters.xero_adapter import XeroFetchAdapter
from core.integrations.oauth.integration_oauth import IntegrationOAuth
from core.integrations.oauth.xero_oauth import (
    xero_integration_oauth,
)
from core.schemas.integrations import IntegrationProvider


# dynamically created list of integrations from the type
INTEGRATIONS: tuple[IntegrationProvider, ...] = get_args(IntegrationProvider)

ADAPTERS: dict[IntegrationProvider, Callable[[str], FetchAdapter]] = {}
INTEGRATION_OAUTH: dict[IntegrationProvider, Callable[[str], IntegrationOAuth]] = {}


def _register_integration(adapter: FetchAdapter.__class__):
    ADAPTERS[adapter.integration()] = lambda workspace_id: adapter(workspace_id)


def _register_integration_oauth(oauth: IntegrationOAuth.__class__):
    INTEGRATION_OAUTH[oauth.integration()] = lambda: oauth()


def setup_integrations(app: FastAPI):
    """
    Run on application start to register applications etc.
    """
    _register_integration(XeroFetchAdapter)

    app.include_router(xero_integration_oauth.router)

    # todo add register integration oauth
