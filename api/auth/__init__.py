from flask import Blueprint
from flask_restful import Api

auth_bp = Blueprint(
    'auth',
    __name__
)

auth_api = Api(auth_bp)

from .views import Login
from .views import Logout
from .views import Register


auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')
auth_api.add_resource(Logout, '/logout')
