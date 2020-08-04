from api.auth.models import User, Token
from api.auth.services import create_user
from api.auth.services import get_or_create_token
from api.auth.services import delete_user_token
from api.auth.selectors import get_user_with_token


def test_given_username_password_create_user_creates_new_user(init_database):
    username = 'testing_user_service'
    password = 'secret_pass'
    initial_user_count = User.query.count()
    user = create_user(
        username=username, password=password
    )
    assert isinstance(user, User)
    assert user.username == username
    assert not user.password == password
    assert user.active is True
    assert User.query.count() == initial_user_count + 1


def test_given_username_having_token_get_or_create_token_returns_existing_token(init_database):
    username = 'testing_user1'
    user_with_token = get_user_with_token(username)
    assert user_with_token.token is not None

    token = get_or_create_token(username)
    assert isinstance(token, Token)
    assert token == user_with_token.token
    

def test_given_username_without_token_get_or_create_token_returns_new_token(new_user):
    username = 'new_testing_user'
    initial_token_count = Token.query.count()
    user_without_token = get_user_with_token(username)
    assert user_without_token.token is None

    token = get_or_create_token(username)
    user_with_token = get_user_with_token(username)
    assert isinstance(token, Token)
    assert token == user_with_token.token
    assert Token.query.count() == initial_token_count + 1


def test_given_a_user_having_token_delete_token_deletes_token(new_user_with_token):
    username = 'new_user_with_token'
    user_with_token = get_user_with_token(username)
    initial_user_count = User.query.count()
    initial_token_count = Token.query.count()
    assert user_with_token.token is not None

    delete_user_token(user_with_token)
    user_without_token = get_user_with_token(username)
    assert user_without_token.token is None
    assert Token.query.count() == initial_token_count - 1
    assert User.query.count() == initial_user_count