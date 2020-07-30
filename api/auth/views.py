from flask import request
from flask_restful import Resource
from marshmallow import fields, Schema
from marshmallow import validates_schema, ValidationError
from marshmallow.validate import Length

from .services import create_user
from .services import get_or_create_token
from .security import verify_password
from .validators import username_is_unique
from .selectors import get_user_by_username


class Register(Resource):

    class InputSchema(Schema):
        username = fields.Str(
            required=True, 
            validate=[Length(max=100), username_is_unique])
        password = fields.Str(required=True, validate=Length(min=8, max=255))
        retype_password = fields.Str(required=True)
        first_name = fields.Str(required=False, validate=Length(max=100))
        last_name = fields.Str(required=False, validate=Length(max=100))

        @validates_schema
        def validate_retype_password(self, data, **kwargs):
            errors = {}
            if data['password'] != data['retype_password']:
                errors['retype_password'] = ["'retype_password' and 'password' do not match"]
                raise ValidationError(errors)


    class OutputSchema(InputSchema):
        class Meta:
            fields = ('username', 'first_name', 'last_name')


    def post(self):
        input_schema = Register.InputSchema()
        errors = input_schema.validate(request.form)

        if errors:
            return errors, 400

        user = create_user(
            request.form['username'],
            request.form['password'],
            request.form.get('first_name'),
            request.form.get('last_name')
        )
        output_schema = Register.OutputSchema()
        return output_schema.dump(user), 201


class Login(Resource):

    class InputSchema(Schema):
        username = fields.Str(required=True)
        password = fields.Str(required=True)

        @validates_schema
        def validate_username_password(self, data, **kwargs):
            user = get_user_by_username(data['username'])
            if user:
                if not verify_password(data['password'], user.password):
                    raise ValidationError('Incorrect Username or Password')

            else:
                raise ValidationError('Incorrect Username or Password')


    class OutputSchema(Schema):
        auth_token = fields.Str(required=True)


    def post(self):
        input_schema = Login.InputSchema()
        errors = input_schema.validate(request.form)

        if errors:
            if '_schema' in errors:
                return {'error': 'Incorrect Username or Password'}, 400
            return errors, 400

        token = get_or_create_token(request.form['username'])
        output_schema = Login.OutputSchema()
        return output_schema.dump(token), 200


class Logout(Resource):
    def get(self):
        return {'message': 'Logged Out'}
