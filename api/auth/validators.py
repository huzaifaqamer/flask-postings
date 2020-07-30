from marshmallow import ValidationError

from .selectors import get_user_by_username


def username_is_unique(data):
    user = get_user_by_username(data)
    if user:
        raise ValidationError('username already exists')