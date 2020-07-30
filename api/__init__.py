from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config.get_configs import get_app_config


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_app_config())
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)  # sqlalchemy
    migrate.init_app(app, db)  # migrate
    ma.init_app(app)  # marshmallow

def register_blueprints(app):
    from api.auth import auth_bp

    app.register_blueprint(auth_bp)

