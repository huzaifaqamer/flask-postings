from flask import request
from flask_restful import Resource
from marshmallow import fields, Schema

from .models import Post
from .services import create_post
from .selectors import get_posts
from api.common import token_required
from api.common import validate_token_header


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

    class ListOutputSchema(OutputSchema):
        fields = ('id', 'title', 'status', 'created_on')

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


    def get(self):
        token = request.headers.get('Authorization')
        kwargs = {}
        if token:
            user, error = validate_token_header(token)
            if error:
                return error[0], error[1]
            
            kwargs['user'] = user
            kwargs['user_posts_only'] = request.args.get('filter') == 'mine'

        posts = get_posts(**kwargs)
        output_schema = ListCreatePost.ListOutputSchema(many=True)
        return output_schema.dump(posts), 200
