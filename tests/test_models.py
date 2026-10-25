from app.models import User


def test_user_model_fields():
    user = User(
        name="Ada Lovelace",
        email="ada@example.com",
        password_hash="hashed-password",
    )

    assert user.id is None
    assert user.name == "Ada Lovelace"
    assert user.email == "ada@example.com"
    assert user.password_hash == "hashed-password"
