from xero_python.api_client import ApiClient
from xero_python.api_client.oauth2 import TokenApi


async def refresh_oauth2_token(api_client: ApiClient):
    oauth2_token = api_client.configuration.oauth2_token
    oauth2_token.update_token(**api_client.get_oauth2_token())

    # cannot refresh
    if not oauth2_token.can_refresh_access_token():
        return None

    # perform refresh flow
    token_api = TokenApi(api_client, oauth2_token.client_id, oauth2_token.client_secret)
    new_token = oauth2_token.fetch_access_token(token_api)
    oauth2_token.update_token(**new_token)
    api_client.set_oauth2_token(new_token)
    return api_client.get_oauth2_token()
