import json


def test_logged_in_user_can_logout(test_client, user_with_hashed_password):
    headers = {
        'Authorization': 'Token secret_token_3'
    }

    response = test_client.delete(
        '/logout', headers=headers
    )
    
    assert response.status_code == 204
    assert response.data == b''

    # testing same token cannot be used after logout
    response = test_client.delete(
        '/logout', headers=headers
    )

    assert response.status_code == 401
    assert b'Provided token is invalid' in response.data


def test_non_logged_in_user_cannot_logout(test_client, new_user):
    response = test_client.delete(
        '/logout'
    )
    
    assert response.status_code == 401
    assert b'Authorization token not provided' in response.data
