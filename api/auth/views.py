from . import auth_bp

@auth_bp.route('/login', strict_slashes=False)
def login():
    return {'message': 'Logged In'}
