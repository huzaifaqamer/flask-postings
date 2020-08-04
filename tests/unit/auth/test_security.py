from api.auth.security import hash_password
from api.auth.security import verify_password


def test_hash_password_modifies_password():
    password = 'secret_password'
    hashed = hash_password(password)
    assert not password == hashed
    assert isinstance(hashed, str)


def test_hash_password_creates_unique_hashes_for_same_input():
    password = 'secret_password'
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    hash3 = hash_password(password)
    assert not hash1 == hash2
    assert not hash1 == hash3
    assert not hash2 == hash3


def test_verify_password_verifies_correct_hashes_only():
    password1 = 'password1'
    password2 = 'password2'
    hash1 = hash_password(password1)
    hash2 = hash_password(password2)
    assert verify_password(password1, hash1)
    assert verify_password(password2, hash2)
    assert not verify_password(password1, hash2)
    assert not verify_password(password2, hash1)