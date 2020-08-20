from flask import request
from flask_restful import Resource
from marshmallow import fields, Schema

from .models import Post
from .services import create_post
from api.common import token_required


class ListCreatePost(Resource):
    
    class InputSchema(Schema):
        title = fields.Str(required=True)
        body = fields.Str(required=True)
        status = fields.Str()

    class OutputSchema(Schema):
        id = fields.Int()
        title = fields.Str()
        body = fields.Str()
        status = fields.Str()
        created_on = fields.DateTime()

    @token_required
    def post(self):
        input_schema = ListCreatePost.InputSchema()
        errors = input_schema.validate(request.form)

        if errors:
            return errors, 400
        
        post = create_post(
            title=request.form['title'],
            body=request.form['body'],
            status=request.form.get('status'),
            author=request.user
        )
        output_schema = ListCreatePost.OutputSchema()
        return output_schema.dump(post), 201
