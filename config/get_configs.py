import os

class BaseConfig():
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SECRET_KEY = 'bTpzM2z58K87bxD$I%^foA$5jnIAlsBFoXZB7!yHFALjWi5tUiG!hXiZ1Zj'
    HOST = '127.0.0.1'


class ProductionConfig(BaseConfig):
    DEBUG = False
    HOST = '0.0.0.0'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'


class TestingConfig(BaseConfig):
    TESTING = True
    ENV = 'testing'


def get_app_config():
    _env_map = {
        'production': ProductionConfig,
        'development': DevelopmentConfig,
        'testing': TestingConfig
    }
    env_name = os.environ['APP_SETTINGS']

    config = _env_map[env_name]()
    return config
