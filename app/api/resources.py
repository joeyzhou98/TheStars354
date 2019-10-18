"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request, redirect
from flask_restplus import Resource

from .security import require_auth
from . import api_rest
from .models import *


class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]


@api_rest.route('/resource/<string:resource_id>')
class ResourceOne(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}

    def post(self, resource_id):
        json_payload = request.json
        return {'timestamp': json_payload}, 201


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Secure Resource Class: Inherit from SecureResource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}


# TODO add logic after deciding the authentication method
@api_rest.route('/registration/')
class UserRegistration(SecureResource):
    def get(self):
        return {'message': 'Hit the user registration endpoint, show the registration page.'}

    def post(self):
        username = request.args['username']
        email = request.args['email']
        password = request.args['password']

        if UserAuthModel.find_by_username(username):
            return {'message': 'User name exists.'}

        if UserAuthModel.find_by_useremail(email):
            return {'message': 'User email exists.'}

        new_user = UserAuthModel(username=username, useremail=email, password=password)
        new_user.save_to_db()
        timestamp = datetime.utcnow().isoformat()
        return {'message': 'saved to database', 'timestamp': timestamp}


# TODO add logic after deciding the authentication method
@api_rest.route('/login/')
class UserLogin(SecureResource):
    def get(self):
        return {'message': 'Hit the user login endpoint with GET, show the login page'}

    def post(self):
        username = request.args['username']
        password = request.args['password']
        login = UserAuthModel.query.filter_by(username=username, password=password).first()
        if login is not None:
            return redirect('/')


@api_rest.route('/logout/access')
class LogoutAccess(SecureResource):
    def post(self):
        return {'message': 'Hit the user logout access endpoint.'}


@api_rest.route('/logout/refresh')
class LogoutRefresh(SecureResource):
    def post(self):
        return {'message': 'Hit the user logout refresh endpoint.'}


@api_rest.route('/token/refresh')
class TokenRefresh(SecureResource):
    def post(self):
        return {'message': 'Hit the token refresh endpoint.'}


@api_rest.route('/password/reset')
class ResetPassword(SecureResource):
    def post(self):
        return {'message': 'Hit the user password reset endpoint.'}
