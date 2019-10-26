from app.api.models import *

db.drop_all()
db.create_all()
admin = UserAuthModel(uid=111, username="admin", useremail="admin@concordia.ca", password="admin")
admin.save_to_db()

buyer = UserAuthModel(uid=444, username="buyer1", useremail="buyer1@concordia.ca", password="buyer1")
buyer.save_to_db()

seller = UserAuthModel(uid=333, username="seller", useremail="seller@concordia.ca", password="seller")
seller.save_to_db()

item1 = Item(item_id=123, item_name="item1", price=20, category="Book", subcategory="aaa", brand="brand1",
             description="description1", seller_id=333, quantity=40, images="url")
item1.save_to_db()
item2 = Item(item_id=133, item_name="item2", price=10, category="Book", subcategory="bbb", brand="brand1",
             description="description2", seller_id=333, quantity=30, images="url2")
item2.save_to_db()

order = Order(order_id=23, buyer_id=444)
order.save_to_db()
order.add_item(item1)
