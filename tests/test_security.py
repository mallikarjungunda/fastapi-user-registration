from app.security import hash_password, verify_password


def test_hash_password_does_not_return_plaintext():
    password = "a-long-password"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)


def test_verify_password_rejects_wrong_password():
    hashed_password = hash_password("correct-password")

    assert not verify_password("incorrect-password", hashed_password)
