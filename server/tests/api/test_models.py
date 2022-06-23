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


def test_is_admin_true():
    assert False


def test_is_admin_false():
    assert False


def test_is_editor_true():
    assert False


def test_is_editor_false():
    assert False


def test_is_viewer_true():
    assert False


def test_is_viewer_false():
    assert False


def test_set_admin():
    assert False


def test_set_admin_non_existing_user():
    assert False


def test_add_editor_to_model():
    assert False


def test_add_editor_to_model_non_existing_user():
    assert False


def test_add_viewer_to_model():
    assert False


def test_add_viewer_to_model_non_existing_user():
    assert False


def test_remove_viewer_from_model():
    assert False


def test_remove_viewer_from_model_non_existing_user():
    assert False


def test_remove_editor_from_model():
    assert False


def test_remove_editor_from_model_non_existing_user():
    assert False
