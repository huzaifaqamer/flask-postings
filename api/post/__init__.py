from flask import Blueprint
from flask_restful import Api

from .models import Post


post_bp = Blueprint(
    'post',
    __name__
)

post_api = Api(post_bp)