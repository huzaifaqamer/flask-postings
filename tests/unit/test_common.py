from unittest import mock
from api.common import __get_user_from_token
from api.common import token_required
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


@mock.patch('api.common.request')
def test_auth_fail_if_header_missing_token_required(mock_request):
    m = mock.Mock()
    func = token_required(m)
    mock_request.headers = {}
    expected_response = {'error': 'Authorization token not provided'}
    response = func()
    assert response[0] == expected_response
    assert response[1] == 401
    assert not m.called


@mock.patch('api.common.request')
def test_auth_fail_if_header_malformed_token_required(mock_request):
    # Token not found in header
    m = mock.Mock()
    func = token_required(m)
    mock_request.headers = {'Authorization': 'Bearer secret_token'}
    expected_response = {'error': "expected 'Token' but got 'Bearer' in 'Authorization' header"}
    response = func()
    assert response[0] == expected_response
    assert response[1] == 400
    assert not m.called

    # token missing in header
    m = mock.Mock()
    func = token_required(m)
    mock_request.headers = {'Authorization': 'Token'}
    expected_response = {'error': "Authorization token not provided"}
    response = func()
    assert response[0] == expected_response
    assert response[1] == 401
    assert not m.called

    # header does not have a space after 'Token'
    m = mock.Mock()
    func = token_required(m)
    mock_request.headers = {'Authorization': 'Tokensecret_token'}
    expected_response = {'error': "expected 'Token' but got 'Tokensecret_token' in 'Authorization' header"}
    response = func()
    assert response[0] == expected_response
    assert response[1] == 400
    assert not m.called


def test_method_called_on_valid_token(init_database):
    mock_request = mock.MagicMock()
    mock_request.headers = {'Authorization': 'Token secret_token_1'}

    with mock.patch('api.common.request', mock_request):
        m = mock.Mock()
        func = token_required(m)
        response = func(m)
        assert m.called