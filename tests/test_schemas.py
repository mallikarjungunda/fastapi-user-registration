import pytest
from pydantic import ValidationError

from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate


def test_user_create_accepts_valid_input():
    payload = UserCreate(
        name="Ada",
        email="ada@example.com",
        password="a-valid-password",
    )

    assert payload.name == "Ada"
    assert payload.email == "ada@example.com"
    assert payload.password == "a-valid-password"


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "", "email": "ada@example.com", "password": "a-valid-password"},
        {"name": "   ", "email": "ada@example.com", "password": "a-valid-password"},
        {"name": "A" * 101, "email": "ada@example.com", "password": "a-valid-password"},
        {"name": "Ada", "email": "not-an-email", "password": "a-valid-password"},
        {"name": "Ada", "email": "ada@example.com", "password": "short"},
        {"name": "Ada", "email": "ada@example.com", "password": "p" * 129},
        {
            "name": "Ada",
            "email": "ada@example.com",
            "password": "a-valid-password",
            "unexpected": True,
        },
    ],
)
def test_user_create_rejects_invalid_input(payload):
    with pytest.raises(ValidationError):
        UserCreate.model_validate(payload)


def test_user_update_accepts_valid_name():
    payload = UserUpdate(name="Ada")

    assert payload.name == "Ada"


@pytest.mark.parametrize("name", ["", "   ", "A" * 101])
def test_user_update_rejects_invalid_name(name):
    with pytest.raises(ValidationError):
        UserUpdate(name=name)


def test_user_update_rejects_extra_fields():
    with pytest.raises(ValidationError):
        UserUpdate.model_validate({"name": "Ada", "email": "ada@example.com"})


def test_user_response_serializes_model_without_password_hash():
    user = User(
        id=1,
        name="Ada",
        email="ada@example.com",
        password_hash="must-not-be-returned",
    )

    response = UserResponse.model_validate(user)

    assert response.model_dump() == {
        "id": 1,
        "name": "Ada",
        "email": "ada@example.com",
    }
