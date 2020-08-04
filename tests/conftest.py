import os
import pytest
from api import create_app
from api import db
from api.auth.models import User, Token


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
    token = Token(auth_token='secret_token', user=user)

    db.session.add(user)
    db.session.add(token)
    db.session.commit()

    yield db

    db.drop_all()