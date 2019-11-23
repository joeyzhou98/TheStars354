""" Security Related things """
from functools import wraps
from flask import request
from flask_restplus import abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
import jwt


def require_auth(func):
    """ Secure method decorator """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verify if User is Authenticated
        # Authentication logic goes here
        if request.headers.get('authorization'):
            return func(*args, **kwargs)
        else:
            return abort(401)

    return wrapper


def admin_required(func):
    """ admin feature decorator """

    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            abort(403, "Admin only")
        else:
            return func(*args, **kwargs)

    return wrapper


def generate_encoded_token(payload, secret, algorithm):
    return jwt.encode(payload, secret, algorithm)


def decode_token(encodedToken, secret, algorithm):
    return jwt.decode(encodedToken, secret, algorithm)
