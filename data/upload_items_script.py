import json
import random
from app.api.models import Item
from app import db

with open("items.json", "r") as f:
    items = json.load(f)

db.create_all()

for item in items:
    quantity = random.randrange(9) + 1
    db.session.add(Item(item_name=item["name"],
                        price=item["price"],
                        category=item["category"],
                        subcategory=item["subcategory"],
                        brand=item["brand"],
                        description=item["description"],
                        quantity=quantity,
                        quantity_sold=random.randrange(quantity),
                        discount=random.uniform(0, 1),
                        images="https://comp354.s3.us-east-2.amazonaws.com/itemPic/" + item["picture"]))

db.session.commit()

