from api.auth.models import User
from api.auth.selectors import get_user_with_token
from api.auth.selectors import get_user_by_username


def test_given_username_get_user_by_username_returns_user(init_database):
    username = 'testing_user1'
    user = get_user_by_username(username)
    assert isinstance(user, User)
    assert user.username == 'testing_user1'


def test_given_invalid_username_get_user_by_username_returns_none(init_database):
    username = 'invalid_user'
    user = get_user_by_username(username)
    assert user is None
    

def test_given_username_get_user_with_token_returns_user_with_token(init_database):
    username = 'testing_user1'
    user = get_user_with_token(username)
    assert isinstance(user, User)
    assert user.username == 'testing_user1'
    assert hasattr(user, 'token')
    assert user.token.auth_token == 'secret_token'


def test_given_invalid_username_get_user_with_token_returns_none(init_database):
    username = 'invalid_user'
    user = get_user_with_token(username)
    assert user is None