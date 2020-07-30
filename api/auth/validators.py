from marshmallow import ValidationError

from .models import User


def username_is_unique(data):
    user = User.query.filter_by(username=data).first()
    if user:
        raise ValidationError('username already exists')