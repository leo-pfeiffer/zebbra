from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from core.schemas.users import RegisterUser
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Zebbra!"}


def test_register():
    user = RegisterUser(**{
        "username": "new_user@example.com",
        "email": "new_user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "workspace": "ACME Inc.",
        "password": "secret"
    })

    response = client.post('/register', data=jsonable_encoder(user))

    assert response.status_code == 200
    assert response.json()['username'] == "new_user@example.com"


def test_cannot_register_existing_username():
    user = RegisterUser(**{
        "username": "johndoe@example.com",
        "email": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "workspace": "ACME Inc.",
        "password": "secret"
    })

    response = client.post("/register", data=jsonable_encoder(user))

    assert response.status_code == 409
