from flask import Flask
from config.get_configs import get_app_config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_app_config())
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)  # sqlalchemy


def register_blueprints(app):
    from api.auth import auth_bp

    app.register_blueprint(auth_bp)

