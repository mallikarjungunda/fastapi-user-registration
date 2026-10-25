from pwdlib import PasswordHash

_password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a password using the recommended algorithm."""
    return _password_hasher.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return _password_hasher.verify(password, hashed_password)