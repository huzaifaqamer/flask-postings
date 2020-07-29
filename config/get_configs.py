import os
from pathlib import Path

current_path = os.path.abspath(os.path.dirname(__file__))
path = Path(current_path)
basedir = path.parent

class BaseConfig():
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SECRET_KEY = 'bTpzM2z58K87bxD$I%^foA$5jnIAlsBFoXZB7!yHFALjWi5tUiG!hXiZ1Zj'
    HOST = '127.0.0.1'

    # SQLALCHEMY settings
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/sqlite.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-User settings
    USER_APP_NAME = "Postings App" 
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    HOST = '0.0.0.0'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'


class TestingConfig(BaseConfig):
    TESTING = True
    ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/test_sqlite.db'


def get_app_config():
    _env_map = {
        'production': ProductionConfig,
        'development': DevelopmentConfig,
        'testing': TestingConfig
    }
    env_name = os.environ['APP_SETTINGS']

    config = _env_map[env_name]()
    return config
