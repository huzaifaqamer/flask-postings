import pytest
from marshmallow import ValidationError

from api.auth.validators import username_is_unique


def test_given_a_username_exists_username_is_unique_raises_error(init_database):
    username = 'testing_user1'
    with pytest.raises(ValidationError) as excinfo:
        username_is_unique(username)

    assert str(excinfo.value) == "username already exists"


def test_given_a_non_existing_username_username_is_unique_returns_none(init_database):
    username = 'non_existing_user'
    output = username_is_unique(username)

    assert output is None