from passlib.context import CryptContext

from api import db
from .models import User


def _hash_password(password):
    crypt_context = CryptContext(schemes=['bcrypt_sha256'])
    return crypt_context.hash(password)


def _verify_password(password, pwd_hash):
    crypt_context = CryptContext(schemes=['bcrypt_sha256'])
    return crypt_context.verify(password, pwd_hash)


def create_user(
    username,
    password,
    first_name=None,
    last_name=None
):
    user = User(
        username=username,
        password=_hash_password(password),
        first_name=first_name,
        last_name=last_name,
        active=True
    )

    db.session.add(user)
    db.session.commit()

    return user