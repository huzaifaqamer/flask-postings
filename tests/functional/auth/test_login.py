import json


def test_can_login_with_valid_credentials(test_client, user_with_hashed_password):
    request_data = {
        'username': 'new_user_with_hashed_password',
        'password': 'secret_password'
    }
    expected_response = {
        'auth_token': 'secret_token'
    }

    response = test_client.post(
        '/login', data=request_data
    )
    
    assert response.status_code == 200
    assert json.loads(response.data) == expected_response


def test_password_must_be_correct(test_client, user_with_hashed_password):
    request_data = {
        'username': 'new_user_with_hashed_password',
        'password': 'wrong_password'
    }

    response = test_client.post(
        '/login', data=request_data
    )
    
    assert response.status_code == 400
    assert b'Incorrect Username or Password' in response.data


def test_username_must_be_correct(test_client, user_with_hashed_password):
    request_data = {
        'username': 'wrong_username',
        'password': 'secret_password'
    }

    response = test_client.post(
        '/login', data=request_data
    )
    
    assert response.status_code == 400
    assert b'Incorrect Username or Password' in response.data


def test_username_is_required(test_client, init_database):
    request_data = {
        'password': 'secret_password'
    }

    response = test_client.post(
        '/login', data=request_data
    )
    
    assert response.status_code == 400
    assert b'Missing data for required field.' in response.data


def test_password_is_required(test_client, init_database):
    request_data = {
        'username': 'failing_username'
    }

    response = test_client.post(
        '/login', data=request_data
    )
    
    assert response.status_code == 400
    assert b'Missing data for required field.' in response.data