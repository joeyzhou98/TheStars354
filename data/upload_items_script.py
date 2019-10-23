import json
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ..app.api.models import Item

app = Flask(__name__, static_folder='../dist/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://comp354:Ll88050517@comp354.cha9oynmedpn.us-east-2.rds.amazonaws.com:3306/comp354'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with open("items.json", "r") as f:
    items = json.load(f)

db.create_all()

for item in items:
    db.session.add(Item(item_name=item["name"],
                        price=item["price"],
                        category=item["category"],
                        brand=item["brand"],
                        description=item["description"][0:1000],
                        quantity=random.randrange(9) + 1,
                        images=item["picture"]))

db.session.commit()

