import pytest
from sqlalchemy.exc import IntegrityError

from api import db
from api.post.models import Post
from api.auth.selectors import get_user_by_username


def test_title_field_required(post_user):
    author = get_user_by_username('post_user')
    failing_post = Post(body='Testing', author=author)
    db.session.add(failing_post)

    with pytest.raises(IntegrityError) as excinfo:
        db.session.commit()

    assert 'NOT NULL constraint failed: post.title' in str(excinfo.value) 


def test_body_field_required(post_user):
    author = get_user_by_username('post_user')
    failing_post = Post(title='Testing', author=author)
    db.session.add(failing_post)

    with pytest.raises(IntegrityError) as excinfo:
        db.session.commit()
    assert 'NOT NULL constraint failed: post.body' in str(excinfo.value)


def test_author_field_required(post_user):
    failing_post = Post(title='Testing', body='Testing')
    db.session.add(failing_post)

    with pytest.raises(IntegrityError) as excinfo:
        db.session.commit()
    assert 'NOT NULL constraint failed: post.user_id' in str(excinfo.value) 


def test_post_created_with_minimum_fields(post_user):
    title = 'Test'
    body = 'Testing Post'
    author = get_user_by_username('post_user')
    post = Post(title=title, body=body, author=author)
    db.session.add(post)
    db.session.commit()
    
    new_post = Post.query.filter_by(title='Test').first()
    assert new_post.title == title
    assert new_post.body == body
    assert new_post.author == author


def test_default_values(post_user):
    author = get_user_by_username('post_user')
    post = Post(title='Testing', body='Test Body', author=author)
    db.session.add(post)
    db.session.commit()

    new_post = Post.query.filter_by(title='Testing').first()
    assert new_post.status == Post.DRAFT
    assert new_post.created_on is not None
    assert new_post.modified_on is not None


def test_status_can_have_choices_only(post_user):
    author = get_user_by_username('post_user')

    with pytest.raises(KeyError) as excinfo:
        post = Post(
            title='Testing',
            body='Test Body', 
            status='ABC',
            author=author
        )
    
    assert 'ABC' in str(excinfo.value) 


def test_cascade_delete(post_user):
    author = get_user_by_username('post_user')
    post = Post(title='Testing', body='Test Body', author=author)
    db.session.add(post)
    db.session.commit()

    db.session.delete(author)
    db.session.commit()

    new_post = Post.query.filter_by(title='Testing').first()
    assert new_post is None