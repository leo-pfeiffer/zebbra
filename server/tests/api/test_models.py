from starlette import status
from starlette.testclient import TestClient

from main import app
from tests.utils import assert_unauthorized_login_checked


def test_model_protected():
    assert_unauthorized_login_checked("/model")


def test_more_than_one_param(access_token):
    client = TestClient(app)
    response = client.get(
        "/model/?user=true&id=some_random_id",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_no_param(access_token):
    client = TestClient(app)
    response = client.get(
        "/model",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_by_id(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0a"
    response = client.get(
        f"/model/?id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["_id"] == model_id


def test_get_id_forbidden(access_token):
    client = TestClient(app)
    model_id = "62b488ba433720870b60ec0b"
    response = client.get(
        f"/model/?id={model_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_workspace(access_token):
    client = TestClient(app)
    wsp = "ACME Inc."
    response = client.get(
        f"/model/?workspace={wsp}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 1
    for m in response.json():
        assert m["meta"]["workspace"] == wsp


def test_get_workspace_forbidden(access_token):
    client = TestClient(app)
    wsp = "Boring Co."
    response = client.get(
        f"/model/?workspace={wsp}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_user(access_token):
    client = TestClient(app)
    response = client.get(
        f"/model/?user=true",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    user = "johndoe@example.com"
    for m in response.json():
        assert (
            (m["meta"]["admin"] == user)
            or (user in m["meta"]["editors"])
            or (user in m["meta"]["viewers"])
        )
