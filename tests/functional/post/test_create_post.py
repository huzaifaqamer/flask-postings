import json
from api.post.models import Post
from api.auth.selectors import get_user_by_username


def test_user_should_be_logged_in_to_create_post(test_client, user_with_hashed_password):

    # failing post
    response = test_client.post(
        '/posts'
    )
    assert response.status_code == 401
    assert b'Authorization token not provided' in response.data

    # successful post
    # also tests that only title and body fields are required
    # to create a post
    data = {
        'title': 'Post 1',
        'body': 'First post'
    }
    headers = {
        'Authorization': 'Token secret_token_3'
    }
    response = test_client.post(
        '/posts', data=data, headers=headers
    )

    received_data = json.loads(response.data)
    assert response.status_code == 201
    assert received_data['title'] == data['title']
    assert received_data['body'] == data['body']
    assert received_data['status'] == Post.DRAFT
    assert 'created_on' in received_data


def test_title_field_required(test_client, user_with_hashed_password):
    data = {
        'body': 'First post'
    }
    headers = {
        'Authorization': 'Token secret_token_3'
    }
    response = test_client.post(
        '/posts', data=data, headers=headers
    )

    assert response.status_code == 400
    assert b"Missing data for required field." in response.data


def test_body_field_required(test_client, user_with_hashed_password):
    data = {
        'title': 'First post'
    }
    headers = {
        'Authorization': 'Token secret_token_3'
    }
    response = test_client.post(
        '/posts', data=data, headers=headers
    )

    assert response.status_code == 400
    assert b"Missing data for required field." in response.data


def test_post_created_with_provided_status(test_client, user_with_hashed_password):
    data = {
        'title': 'Post 1',
        'body': 'First post',
        'status': Post.PUBLISHED
    }
    headers = {
        'Authorization': 'Token secret_token_3'
    }
    response = test_client.post(
        '/posts', data=data, headers=headers
    )

    assert response.status_code == 201
    assert json.loads(response.data)['status'] == data['status']


def test_post_author_is_logged_in_user(test_client, user_with_hashed_password):
    data = {
        'title': 'Post 1',
        'body': 'First post',
        'status': Post.PUBLISHED
    }
    headers = {
        'Authorization': 'Token secret_token_3'
    }
    response = test_client.post(
        '/posts', data=data, headers=headers
    )

    expected_user = get_user_by_username('new_user_with_hashed_password')
    post = Post.query.get(json.loads(response.data)['id'])
    assert post.user_id == expected_user.id