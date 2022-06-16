import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from core.schemas.users import RegisterUser
from main import app
from tests.utils import count_documents

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Zebbra!"}


@pytest.mark.anyio
async def test_register():
    user = RegisterUser(**{
        "username": "new_user@example.com",
        "email": "new_user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "workspace": "ACME Inc.",
        "password": "secret"
    })

    users_initial = await count_documents("users")

    response = client.post('/register', json=jsonable_encoder(user))

    assert response.status_code == 200
    assert response.json()['username'] == "new_user@example.com"
    assert (await count_documents("users") - users_initial) == 1


@pytest.mark.anyio
async def test_cannot_register_existing_username():
    user = RegisterUser(**{
        "username": "johndoe@example.com",
        "email": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "workspace": "ACME Inc.",
        "password": "secret"
    })

    users_initial = await count_documents("users")
    response = client.post("/register", json=jsonable_encoder(user))

    assert response.status_code == 409
    assert await count_documents("users") == users_initial
