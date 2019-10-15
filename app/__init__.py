import os
from flask import Flask, current_app, send_file
from flask_sqlalchemy import SQLAlchemy

from .client import client_bp

app = Flask(__name__, static_folder='../dist/static')
#need to set up database first before import api_bp
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://comp354:Ll88050517@comp354.cha9oynmedpn.us-east-2.rds.amazonaws.com:3306/comp354'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from .api import api_bp

app.register_blueprint(api_bp)
# app.register_blueprint(client_bp)


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


