import json
from unittest import mock
from api.auth.selectors import get_user_by_username


def test_method_called_with_no_arguments_for_logged_out_user(test_client):

    m_get_posts = mock.MagicMock(return_value=[])

    with mock.patch('api.post.views.get_posts', m_get_posts):
        response = test_client.get('/posts')

        assert m_get_posts.called
        args, kwargs = m_get_posts.call_args

        assert args == ()
        assert kwargs == {}

        # checks filter functionality
        response = test_client.get('/posts?filter=mine')

        assert m_get_posts.called
        args, kwargs = m_get_posts.call_args

        assert args == ()
        assert kwargs == {}

def test_method_called_with_user_for_logged_in_user(test_client, users_with_posts):

    m_get_posts = mock.MagicMock(return_value=[])

    with mock.patch('api.post.views.get_posts', m_get_posts):
        headers = {'Authorization': 'Token post_user1_token'}
        response = test_client.get('/posts', headers=headers)

        assert m_get_posts.called
        args, kwargs = m_get_posts.call_args

        assert args == ()
        assert kwargs == {
            'user': get_user_by_username('post_user1'),
            'user_posts_only': False
        }


def test_method_called_with_user_posts_only_argument_for_query_params(test_client, users_with_posts):

    m_get_posts = mock.MagicMock(return_value=[])

    with mock.patch('api.post.views.get_posts', m_get_posts):
        headers = {'Authorization': 'Token post_user2_token'}
        response = test_client.get('/posts?filter=mine', headers=headers)

        assert m_get_posts.called
        args, kwargs = m_get_posts.call_args

        assert args == ()
        assert kwargs == {
            'user': get_user_by_username('post_user2'),
            'user_posts_only': True
        }


def test_output_schema(test_client, users_with_posts):
    required_fields = [
        'id', 'title', 'status', 'created_on'
    ]

    response = test_client.get('/posts')
    posts = json.loads(response.data)
    for post in posts:
        for key in post.keys():
            assert key in required_fields
