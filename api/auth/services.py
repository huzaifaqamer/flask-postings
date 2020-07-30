import os
import binascii

from api import db
from .models import User, Token
from .security import hash_password
from .selectors import get_user_by_username
from .selectors import get_user_with_token


def _generate_token():
    return binascii.hexlify(os.urandom(20)).decode()


def create_user(
    username,
    password,
    first_name=None,
    last_name=None
):
    user = User(
        username = username,
        password = hash_password(password),
        first_name = first_name,
        last_name = last_name,
        active = True
    )

    db.session.add(user)
    db.session.commit()

    return user


def get_or_create_token(username):
    user = get_user_with_token(username)

    if user.token is None:
        token = Token(
            auth_token = _generate_token(),
            user = user
        )

        db.session.add(token)
        db.session.commit()
    else:
        token = user.token

    return token