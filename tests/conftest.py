import os
import random
import datetime

import pytest
from api import create_app
from api import db
from api.auth.models import User, Token
from api.post.models import Post
from api.auth.services import create_user


@pytest.fixture(scope='module')
def test_client():
    os.environ['APP_SETTINGS'] = 'testing'
    flask_app = create_app()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # insert data
    user = User(username='testing_user1', password='secret_password')
    token = Token(auth_token='secret_token_1', user=user)

    db.session.add(user)
    db.session.add(token)
    db.session.commit()

    yield db

    db.drop_all()


@pytest.fixture(scope='module')
def new_user(init_database):
    new_user = User(username='new_testing_user', password='secret_password')
    db.session.add(new_user)
    db.session.commit()

    return new_user


@pytest.fixture(scope='module')
def new_user_with_token(init_database):
    new_user = User(username='new_user_with_token', password='secret_password')
    token = Token(auth_token='secret_token_2', user=new_user)
    db.session.add(new_user)
    db.session.add(token)
    db.session.commit()
    
    return new_user


@pytest.fixture(scope='module')
def user_with_hashed_password(init_database):
    user_data = dict(username='new_user_with_hashed_password', password='secret_password')
    new_user = create_user(**user_data)
    token = Token(auth_token='secret_token_3', user=new_user)
    db.session.add(token)
    db.session.commit()
    
    return new_user


@pytest.fixture(scope='function')
def post_user(init_database):
    user = User(username='post_user', password='secret_password')
    db.session.add(user)
    db.session.commit()

    yield user

    db.session.rollback()
    User.query.delete()
    db.session.commit()


def random_time():
    start = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    end = datetime.datetime.utcnow()

    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

@pytest.fixture(scope='module')
def users_with_posts(init_database):
    user1_data = dict(username='post_user1', password='secret_password')
    user2_data = dict(username='post_user2', password='secret_password')
    user1 = create_user(**user1_data)
    user2 = create_user(**user2_data)
    token1 = Token(auth_token='post_user1_token', user=user1)
    token2 = Token(auth_token='post_user2_token', user=user2)
    user1_post1 = Post(title='Draft Post', body='User 1', status=Post.DRAFT, author=user1, created_on=random_time())
    user1_post2 = Post(title='Published Post', body='User 1', status=Post.PUBLISHED, author=user1, created_on=random_time())
    user1_post3 = Post(title='Unpublished Post', body='User 1', status=Post.UNPUBLISHED, author=user1, created_on=random_time())
    user2_post1 = Post(title='Draft Post', body='User 2', status=Post.DRAFT, author=user2, created_on=random_time())
    user2_post2 = Post(title='Published Post', body='User 2', status=Post.PUBLISHED, author=user2, created_on=random_time())
    user2_post3 = Post(title='Unpublished Post', body='User 2', status=Post.UNPUBLISHED, author=user2, created_on=random_time())
    db.session.add(token1)
    db.session.add(token2)
    db.session.add(user1_post1)
    db.session.add(user1_post2)
    db.session.add(user1_post3)
    db.session.add(user2_post1)
    db.session.add(user2_post2)
    db.session.add(user2_post3)
    db.session.commit()
    
    return user1