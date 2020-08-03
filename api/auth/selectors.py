from sqlalchemy.orm import joinedload

from .models import User


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_with_token(username):
    return User.query.filter_by(
        username=username
        ).options(joinedload('token')).first()