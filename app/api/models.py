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


class UserAuthModel(db.Model):
    __tablename__ = 'userAuthInfo'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    useremail = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_useremail(cls, email):
        return cls.query.filter_by(useremail=email).first()


class BuyerModel(UserAuthModel):
    __tablename__ = "buyerInfo"

    uid = db.Column(db.Integer, db.ForeignKey(UserAuthModel.uid), primary_key=True)
    address1 = db.Column(db.String(120))
    address2 = db.Column(db.String(120))
    address3 = db.Column(db.String(120))
    paypal = db.Column(db.String(20), nullable=False)
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

    @classmethod
    def buyer_exists(cls, uid):
        if cls.query.filter_by(uid=uid).count() == 0:
            return False
        else:
            return True


class SellerModel(UserAuthModel):
    __tablename__ = "sellerInfo"

    uid = db.Column(db.Integer, db.ForeignKey(UserAuthModel.uid), primary_key=True)
    membership_date = db.Column(db.Date, nullable=False)
    offered_products = db.relationship("Item")

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
    items = db.relationship("Item", secondary="orderItem")

    def save_to_db(self):
        if BuyerModel.buyer_exists(self.buyer_id):
            db.session.add(self)
            db.session.commit()
        else:
            print("No such buyer.")

    def add_item(self, item):
        self.items.append(item)
        db.session.commit()


class Review(db.Model):
    __tablename__ = "review"

    review_id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.item_id"))
    content = db.Column(db.String(512), nullable=True)

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
    itemName = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Float, unique=True, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellerInfo.uid"), nullable=False)
    reviews = db.relationship("Review")

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
