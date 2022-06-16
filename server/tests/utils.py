from fastapi.testclient import TestClient
from main import app


def assert_unauthorized_login_checked(endpoint: str) -> None:
    """
    Assert that unauthorized users cannot access an endpoint.
    :param endpoint: Endpoint to check.
    """
    client = TestClient(app)
    response = client.get(endpoint, headers={
            'Authorization': f'Bearer not_a_token'
        })

    assert response.status_code == 401
