import pytest
from pwdlib import PasswordHash
from sqlmodel import select

from app.database import get_session
from app.models import User


def create_user(client, **overrides):
    payload = {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "password": "a-long-test-password",
    }
    payload.update(overrides)
    return client.post("/users", json=payload)


def test_register_user_normalizes_fields_and_hides_password(client):
    response = create_user(
        client,
        name="  Ada Lovelace  ",
        email="Ada@Example.com",
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Ada Lovelace",
        "email": "ada@example.com",
    }
    assert "password" not in response.text
    assert "password_hash" not in response.text


def test_register_user_rejects_duplicate_email_case_insensitively(client):
    assert create_user(client).status_code == 201

    response = create_user(client, email="ADA@example.com")

    assert response.status_code == 409
    assert response.json() == {"detail": "Email is already registered"}


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "", "email": "ada@example.com", "password": "a-long-test-password"},
        {"name": "Ada", "email": "invalid", "password": "a-long-test-password"},
        {"name": "Ada", "email": "ada@example.com", "password": "short"},
        {
            "name": "Ada",
            "email": "ada@example.com",
            "password": "a-long-test-password",
            "unexpected": True,
        },
    ],
)
def test_register_user_validates_input(client, payload):
    response = client.post("/users", json=payload)

    assert response.status_code == 422


def test_register_user_stores_password_hash(client):
    response = create_user(client)
    user_id = response.json()["id"]

    session_dependency = client.app.dependency_overrides[get_session]
    session_generator = session_dependency()
    session = next(session_generator)
    try:
        user = session.exec(select(User).where(User.id == user_id)).one()
        assert PasswordHash.recommended().verify(
            "a-long-test-password",
            user.password_hash,
        )
    finally:
        session_generator.close()


def test_list_users_orders_and_paginates(client):
    for name, email in [
        ("First", "first@example.com"),
        ("Second", "second@example.com"),
        ("Third", "third@example.com"),
    ]:
        assert create_user(client, name=name, email=email).status_code == 201

    response = client.get("/users", params={"offset": 1, "limit": 1})

    assert response.status_code == 200
    assert [user["name"] for user in response.json()] == ["Second"]


@pytest.mark.parametrize("params", [{"offset": -1}, {"limit": 0}, {"limit": 101}])
def test_list_users_rejects_invalid_pagination(client, params):
    response = client.get("/users", params=params)

    assert response.status_code == 422


def test_get_user_returns_existing_user(client):
    user_id = create_user(client).json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_user_returns_404_for_missing_user(client):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_user_trims_name(client):
    user_id = create_user(client).json()["id"]

    response = client.patch(f"/users/{user_id}", json={"name": "  Ada  "})

    assert response.status_code == 200
    assert response.json()["name"] == "Ada"


def test_update_user_returns_404_for_missing_user(client):
    response = client.patch("/users/999", json={"name": "Ada"})

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.parametrize("payload", [{"name": ""}, {"name": "   "}, {"email": "x"}])
def test_update_user_validates_input(client, payload):
    user_id = create_user(client).json()["id"]

    response = client.patch(f"/users/{user_id}", json=payload)

    assert response.status_code == 422


def test_delete_user_removes_existing_user(client):
    user_id = create_user(client).json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204
    assert client.get(f"/users/{user_id}").status_code == 404


def test_delete_user_returns_404_for_missing_user(client):
    response = client.delete("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
