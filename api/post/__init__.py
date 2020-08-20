from flask import Blueprint
from flask_restful import Api

from .models import Post
from .views import CreateRetrievePost


post_bp = Blueprint(
    'post',
    __name__
)

post_api = Api(post_bp)
post_api.add_resource(CreateRetrievePost, '/posts')