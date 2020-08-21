from api.post.models import Post
from api.post.selectors import get_posts
from api.auth.selectors import get_user_by_username


def test_by_default_published_posts_are_returned(users_with_posts):
    posts = get_posts()
    for post in posts:
        assert post.status == Post.PUBLISHED


def test_only_required_fields_are_returned(users_with_posts):
    required_fields = [
        'id', 'title', 'status', 'created_on'
    ]

    posts = get_posts()
    for post in posts:
        for key in post.keys():
            assert key in required_fields


def test_all_user_posts_are_included(users_with_posts):
    author1 = get_user_by_username('post_user1')
    posts = get_posts(user=author1)
    post_ids = [post.id for post in posts]

    published_post_ids = Post.query.with_entities(
        Post.id).filter_by(status=Post.PUBLISHED).values()

    user_post_ids = Post.query.with_entities(
        Post.id).filter_by(user_id=author1.id).values()

    assert all([post_id in post_ids for post_id in published_post_ids])
    assert all([post_id in post_ids for post_id in user_post_ids])


def test_result_sorted_by_created_on(users_with_posts):
    author2 = get_user_by_username('post_user2')
    posts = get_posts(user=author2)

    print(posts)
    for idx, post in enumerate(posts):
        try:
            next_post = posts[idx+1]
            timedelta = post.created_on - next_post.created_on
            assert timedelta.microseconds > 0
        except IndexError:
            pass


def test_user_posts_only_filters_out_posts(users_with_posts):
    author2 = get_user_by_username('post_user2')
    posts = get_posts(user=author2, user_posts_only=True)
    post_ids = [post.id for post in posts]

    user_post_ids = Post.query.with_entities(
        Post.id).filter_by(user_id=author2.id).all()

    assert all([post_id[0] in post_ids for post_id in user_post_ids])
    assert len(post_ids) == len(user_post_ids)