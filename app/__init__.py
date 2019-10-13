import os
from flask import Flask, current_app, send_file, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

from .api import api_bp
from .client import client_bp

app = Flask(__name__, static_folder='../dist/static')
app.register_blueprint(api_bp)
# app.register_blueprint(client_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://comp354:Ll88050517@comp354.cha9oynmedpn.us-east-2.rds.amazonaws.com:3306/comp354'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()
    print('DB CREATED')
    print(db.metadata.tables)


from .config import Config

app.logger.info('>>> {}'.format(Config.FLASK_ENV))


@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)


from .models import *


@app.route('/registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        if UserAuthModel.find_by_username(uname):
            return {'message': 'User name exists.'}

        if UserAuthModel.find_by_useremail(mail):
            return {'message': 'User email exists.'}

        new_user = UserAuthModel(username=uname, useremail=mail, password=passw)
        new_user.save_to_db()
        return {'message': 'saved to database'}
    return {'message': 'Hit the user registration endpoint, show the registration page.'}


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == "POST":
        uemail = request.form['uname']
        passw = request.form['passw']

        login = UserAuthModel.query.filter_by(uemail=UserAuthModel.username, passw=UserAuthModel.password).first()
        if login is not None:
            return redirect('/')
    return {'message': 'Hit the user login endpoint with GET, show the login page'}


@app.route('/logout/access', methods=['POST'])
def logout_access():
    return {'message': 'Hit the user logout access endpoint.'}


@app.route('/logout/refresh', methods=['POST'])
def logout_refresh():
    return {'message': 'Hit the user logout refresh endpoint.'}


@app.route('/token/refresh', methods=['POST'])
def token_refresh():
    return {'message': 'Hit the token refresh endpoint.'}


@app.route('/password/reset', methods=['POST'])
def reset_password():
    return {'message': 'Hit the user password reset endpoint.'}
