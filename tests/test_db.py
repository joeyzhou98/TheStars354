from app.api.models import *

db.drop_all()
db.create_all()
admin = UserAuthModel(uid=111, username="admin", useremail="admin@concordia.ca", password="admin")
admin.save_to_db()

buyer = BuyerModel(uid=444, username="buyer1", useremail="buyer1@concordia.ca", password="buyer1", paypal="paypal1")
buyer.save_to_db()

seller = SellerModel(uid=333, username="seller", useremail="seller@concordia.ca", password="seller",
                     membership_date="2019-11-11")
seller.save_to_db()

item1 = Item(item_id=123, itemName="item1", price=20, category="Book", brand="brand1",
             description="description1", seller_id=333)
item1.save_to_db()
item2 = Item(item_id=133, itemName="item2", price=10, category="Bok", brand="brand1",
             description="description2", seller_id=333)
item2.save_to_db()

order = Order(order_id=23, buyer_id=444)
order.save_to_db()
buyer.add_to_wish_list(item1)
buyer.add_to_shopping_list(item2)
order.add_item(item1)
seller.add_offered_products(item1)
