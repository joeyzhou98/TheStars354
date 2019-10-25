from app import db

orderItem = db.Table(
    "orderItem",
    db.Column('order_id', db.Integer, db.ForeignKey("order.order_id")),
    db.Column("item_id", db.Integer, db.ForeignKey("item.item_id"))
)

wishListItem = db.Table(
    "wishListItem",
    db.Column('buyer_id', db.Integer, db.ForeignKey("buyerInfo.uid")),
    db.Column("item_id", db.Integer, db.ForeignKey("item.item_id"))
)

shoppingListItem = db.Table(
    "shoppingListItem",
    db.Column('buyer_id', db.Integer, db.ForeignKey("buyerInfo.uid")),
    db.Column("item_id", db.Integer, db.ForeignKey("item.item_id"))
)

orderSeller = db.Table(
    "orderSeller",
    db.Column('order_id', db.Integer, db.ForeignKey("order.order_id")),
    db.Column("seller_id", db.Integer, db.ForeignKey("sellerInfo.uid"))
)


class UserAuthModel(db.Model):
    __tablename__ = 'userAuthInfo'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    useremail = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def save_to_db(self):
        buyer = BuyerModel(uid=self.uid)
        seller = SellerModel(uid=self.uid, membership_date=db.func.current_date())
        db.session.add(self)
        db.session.commit()
        db.session.add(buyer)
        db.session.add(seller)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_useremail(cls, email):
        return cls.query.filter_by(useremail=email).first()


class BuyerModel(db.Model):
    __tablename__ = "buyerInfo"

    uid = db.Column(db.Integer, db.ForeignKey(UserAuthModel.uid), primary_key=True)
    address1 = db.Column(db.String(120))
    address2 = db.Column(db.String(120))
    address3 = db.Column(db.String(120))
    paypal = db.Column(db.String(20))
    order_history = db.relationship("Order")
    wish_list = db.relationship("Item", secondary=wishListItem)
    shopping_list = db.relationship("Item", secondary=shoppingListItem)
    review_list = db.relationship("Review")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def add_to_wish_list(self, item):
        self.wish_list.append(item)
        db.session.commit()

    def add_to_shopping_list(self, item):
        self.shopping_list.append(item)
        db.session.commit()

    def set_paypal(self, paypal):
        BuyerModel.query.filter_by(uid=self.uid).first().paypal = paypal
        db.session.commit()

    @classmethod
    def buyer_exists(cls, uid):
        if cls.query.filter_by(uid=uid).count() == 0:
            return False
        else:
            return True


class SellerModel(db.Model):
    __tablename__ = "sellerInfo"

    uid = db.Column(db.Integer, db.ForeignKey(UserAuthModel.uid), primary_key=True)
    membership_date = db.Column(db.Date, nullable=False)
    offered_products = db.relationship("Item")
    orders = db.relationship("Order", secondary=orderSeller)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def add_offered_products(self, item):
        self.offered_products.append(item)
        db.session.commit()

    @classmethod
    def get_offered_products(cls):
        return cls.query.join(SellerModel, Item)

    @classmethod
    def seller_exists(cls, seller_id):
        if cls.query.filter_by(uid=seller_id).count() == 0:
            return False
        else:
            return True


class Order(db.Model):
    __tablename__ = "order"

    order_id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    items = db.relationship("Item", secondary=orderItem)

    def save_to_db(self):
        if BuyerModel.buyer_exists(self.buyer_id):
            db.session.add(self)
            db.session.commit()
        else:
            print("No such buyer.")

    def add_item(self, item):
        db.engine.execute(orderSeller.insert(), order_id=self.order_id, seller_id=item.seller_id)
        self.items.append(item)
        db.session.commit()


class Review(db.Model):
    __tablename__ = "review"

    review_id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.item_id"))
    content = db.Column(db.String(512), nullable=True)
    images = db.Column(db.String(1000))

    def save_to_db(self):
        if BuyerModel.buyer_exists(self.buyer_id):
            print("No such buyer")
        elif Order.order_exists(self.item_id):
            print("No such item")
        else:
            db.session.add(self)
            db.session.commit()


class Item(db.Model):
    __tablename__ = 'item'

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(300), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    subcategory = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False, default=0)
    discount = db.Column(db.Float, nullable=False, default=0.0)
    images = db.Column(db.String(1000), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellerInfo.uid"), nullable=True)
    reviews = db.relationship("Review")

    @property
    def serialize(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "price": self.price,
            "category": self.category,
            "subcategory": self.subcategory,
            "brand": self.brand,
            "description": self.description,
            "quantity": self.quantity,
            "quantity_sold": self.quantity_sold,
            "discount": self.discount,
            "images": self.images,
            "seller_id": self.seller_id
        }


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category)

    @classmethod
    def find_by_brand(cls, brand):
        return cls.query.filter_by(brand=brand)

    @classmethod
    def find_by_price(cls, price):
        return cls.query.filter(cls.price <= price)

    @classmethod
    def item_exists(cls, item_id):
        if cls.query.filter_by(item_id=item_id).count() == 0:
            return False
        else:
            return True
