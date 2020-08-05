import json


def test_user_can_register_with_username_and_password(test_client, init_database):
    request_data = {
        'username': 'new_user',
        'password': 'secret_password',
        'retype_password': 'secret_password'
    }
    expected_response = {
        'username': request_data['username'],
        'first_name': None,
        'last_name': None
    }

    response = test_client.post(
        '/register', data=request_data
    )
    
    assert response.status_code == 201
    assert json.loads(response.data) == expected_response


def test_user_can_register_with_all_fields(test_client, init_database):
    request_data = {
        'username': 'test_user',
        'password': 'secret_password',
        'retype_password': 'secret_password',
        'first_name': 'Test',
        'last_name': 'User'
    }
    expected_response = {
        'username': request_data['username'],
        'first_name': request_data['first_name'],
        'last_name': request_data['last_name']
    }

    response = test_client.post(
        '/register', data=request_data
    )
    
    assert response.status_code == 201
    assert json.loads(response.data) == expected_response


def test_password_not_less_than_8_chars(test_client, init_database):
    request_data = {
        'username': 'failing_username',
        'password': 'secret',
        'retype_password': 'secret'
    }

    response = test_client.post(
        '/register', data=request_data
    )
    
    assert response.status_code == 400
    assert b'Length must be between 8 and 255.' in response.data


def test_password_and_retype_password_must_match(test_client, init_database):
    request_data = {
        'username': 'failing_username',
        'password': 'secret_password',
        'retype_password': 'secret'
    }

    response = test_client.post(
        '/register', data=request_data
    )
    
    assert response.status_code == 400
    assert b"retype_password' and 'password' do not match" in response.data


def test_username_is_required(test_client, init_database):
    request_data = {
        'password': 'secret_password',
        'retype_password': 'secret_password'
    }

    response = test_client.post(
        '/register', data=request_data
    )
    
    assert response.status_code == 400
    assert b"Missing data for required field." in response.data


def test_password_is_required(test_client, init_database):
    request_data = {
        'username': 'failing_username',
        'retype_password': 'secret_password'
    }

    response = test_client.post(
        '/register', data=request_data
    )
    
    assert response.status_code == 400
    assert b"Missing data for required field." in response.data


def test_retype_password_is_required(test_client, init_database):
    request_data = {
        'username': 'failing_username',
        'password': 'secret_password'
    }

    response = test_client.post(
        '/register', data=request_data
    )
    
    assert response.status_code == 400
    assert b"Missing data for required field." in response.data


def test_username_must_be_unique(test_client, init_database):
    request_data = {
        'username': 'testing_user1',
        'password': 'secret_password',
        'retype_password': 'secret_password'
    }

    response = test_client.post(
        '/register', data=request_data
    )
    
    assert response.status_code == 400
    assert b'username already exists' in response.data