from typing import get_args, Callable
import re

from fastapi import FastAPI
from core.integrations.adapters.adapter import FetchAdapter
from core.integrations.adapters.xero_adapter import XeroFetchAdapter
from core.integrations.oauth.gusto_oauth import gusto_integration_oauth
from core.integrations.oauth.integration_oauth import IntegrationOAuth
from core.integrations.oauth.xero_oauth import (
    xero_integration_oauth,
)
from core.schemas.integrations import IntegrationProvider


# dynamically created list of integrations from the type
INTEGRATIONS: tuple[IntegrationProvider, ...] = get_args(IntegrationProvider)

# this is to validate the correct format of the provided integrations
for integration in INTEGRATIONS:
    assert re.fullmatch("[A-Za-z\\d]+", integration)

ADAPTERS: dict[IntegrationProvider, Callable[[str], FetchAdapter]] = {}
INTEGRATION_OAUTH: dict[IntegrationProvider, IntegrationOAuth] = {}


def _register_adapter(adapter: FetchAdapter.__class__):
    ADAPTERS[adapter.integration()] = lambda workspace_id: adapter(workspace_id)


def _register_oauth(oauth: IntegrationOAuth):
    INTEGRATION_OAUTH[oauth.integration()] = oauth


def setup_integrations(app: FastAPI):
    """
    Run on application start to register applications etc.
    """

    # register the FetchAdapter implementation *class* here
    _register_adapter(XeroFetchAdapter)

    # register the IntegrationOAuth implementation *instance* here
    _register_oauth(xero_integration_oauth)
    _register_oauth(gusto_integration_oauth)

    for integration_name in INTEGRATIONS:
        router = INTEGRATION_OAUTH[integration_name].router
        app.include_router(router)
