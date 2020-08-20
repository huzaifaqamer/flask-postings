from api.post.models import Post
from api.post.services import create_post
from api.auth.selectors import get_user_by_username


def test_create_post_creates_new_post(post_user):
    title = 'Testing Post'
    body = 'Thisi is a test'
    status = Post.UNPUBLISHED
    author = get_user_by_username('post_user')

    initial_count = Post.query.count()
    post = create_post(
        title=title,
        body=body,
        status=status,
        author=author
    )
    
    assert isinstance(post, Post)
    assert post.title == title
    assert post.body == body
    assert post.status == status
    assert post.author == author
    assert Post.query.count() == initial_count + 1