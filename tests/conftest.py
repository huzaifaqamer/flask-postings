import os
import pytest
from api import create_app
from api import db
from api.auth.models import User, Token
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
