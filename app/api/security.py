""" Security Related things """
from functools import wraps
from flask import request
from flask_restplus import abort
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


def generate_encoded_token(payload, secret, algorithm):
    return jwt.encode(payload, secret, algorithm)


def decode_token(encodedToken, secret, algorithm):
    return jwt.decode(encodedToken, secret, algorithm)
