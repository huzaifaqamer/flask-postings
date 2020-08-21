from functools import wraps

from flask import request

from api.auth.models import User, Token


def get_user_from_token(token):
    token = Token.query.filter_by(auth_token=token).join(User).first()
    if token:
        return token.user
    
    return None


def token_required(func):
    """
    check request header for presence of 'Authorization'
    header and test the recieved token for its validity.
    If a user is found then adds a user attribute to request object
    """
    @wraps(func)
    def inner_func(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            try:
                splitted_token = token.split()
                if splitted_token[0] != 'Token':
                    return {'error': f"expected 'Token' but got '{splitted_token[0]}' in 'Authorization' header"}, 400
                
                user = get_user_from_token(splitted_token[1])
                if user:
                    request.user = user
                    return func(*args, **kwargs)

                return {'error': 'Provided token is invalid'}, 401
            except IndexError:
                pass
        return {'error': 'Authorization token not provided'}, 401

    return inner_func