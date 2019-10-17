from app import db


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

    paypal = db.Column(db.String(20), nullable=False)

    address = db.relationship("address", back_populates="buyer")
    order_history = db.relationship("order", back_populates="orderNumber")
    review_history = db.relationship("review", back_populates="review")
    wish_list = db.relationship("wishList", back_populates="buyer")

    @classmethod
    def get_address(cls, uid):
        return cls.query.filter_by(uid=uid)

    @classmethod
    def get_order_history(cls, uid):
        return cls.query.filter_by(uid=uid)


class Address(db.Model):
    __tablename__ = "address"

    uid = db.Column(db.Integer, primary_key=True)
    address1 = db.Column(db.String)
    address2 = db.Column(db.String)
    address3 = db.Column(db.String)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Order(db.Model):
    __tablename__ = "order"

    orderNumber = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellerInfo.uid"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("itemInfo.itemId"), nullable=False)

    buyer = db.relationship("buyerInfo", back_populates="uid")
    seller = db.relationship("sellerInfo", back_populates="uid")
    item = db.relationship("itemInfo", back_populates="itemId")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class ShoppingCart(db.Model):
    __tablename__ = "order"

    uid = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("itemInfo.itemId"), nullable=False)

    buyer = db.relationship("buyerInfo", back_populates="address")
    item = db.relationship("itemInfo")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Review(db.Model):
    __tablename__ = "review"

    uid = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("itemInfo.itemId"), nullable=False)

    buyer = db.relationship("buyerInfo", back_populates="address")
    item = db.relationship("itemInfo")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class WishList(db.Model):
    __tablename__ = "wishList"

    uid = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("itemInfo.itemId"), nullable=False)

    buyer = db.relationship("buyerInfo", back_populates="address")
    item = db.relationship("itemInfo")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class ItemModel(db.Model):
    __tablename__ = 'itemInfo'

    itemId = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Float, unique=True, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(512), nullable=True)

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
