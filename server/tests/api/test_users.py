import pytest
from fastapi.testclient import TestClient
from main import app
from tests.utils import assert_unauthorized_login_checked


def test_users_me(access_token):

    client = TestClient(app)
    response = client.get("/user", headers={
            'Authorization': f'Bearer {access_token}'
        })

    assert response.status_code == 200
    assert response.json()['username'] == 'johndoe'


def test_users_me_protected():
    assert_unauthorized_login_checked("/user")
