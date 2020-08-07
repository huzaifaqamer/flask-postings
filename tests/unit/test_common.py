from api.common import __get_user_from_token
from api.auth.models import User


def test_given_invalid_token_get_user_from_token_returns_none(init_database):
    token = 'invalid_token'
    user = __get_user_from_token(token)
    assert user is None


def test_given_valid_token_get_user_from_token_returns_user(init_database):
    token = 'secret_token_1'
    user = __get_user_from_token(token)
    assert isinstance(user, User)
    assert user.username == 'testing_user1'