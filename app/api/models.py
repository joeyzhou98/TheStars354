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

    uid = db.Column(db.Integer, db.ForeignKey(UserAuthModel.uid), primary_key=True)
    paypal = db.Column(db.String(20), nullable=False)
    order_history = db.relationship("order", back_populates="orderNumber")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_address(cls):
        return cls.query.join(Address, BuyerModel)

    @classmethod
    def get_order_history(cls):
        return cls.query.join(Order, BuyerModel)

    @classmethod
    def get_wish_list(cls):
        return cls.query.join(WishList, BuyerModel)

    @classmethod
    def get_shopping_cart(cls):
        return cls.query.join(ShoppingCart, BuyerModel)

    @classmethod
    def get_reviews(cls):
        return cls.query.join(BuyerModel, Review).second


class SellerModel(UserAuthModel):
    __tablename__ = "sellerInfo"

    uid = db.Column(db.Integer, db.ForeignKey(UserAuthModel.uid), primary_key=True)
    membership_date = db.Column(db.Date, nullable=False)
    offered_products = db.relationship("itemInfo")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_offered_products(cls):
        return cls.query.join(SellerModel, ItemModel)


class Address(db.Model):
    __tablename__ = "address"

    uid = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"), primary_key=True)
    address1 = db.Column(db.String(120))
    address2 = db.Column(db.String(120))
    address3 = db.Column(db.String(120))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Order(db.Model):
    __tablename__ = "order"

    orderNumber = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellerInfo.uid"), nullable=False)

    items = db.relationship("itemInfo")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class ShoppingCart(db.Model):
    __tablename__ = "shoppingCart"

    uid = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"), nullable=False, primary_key=True)
    items = db.relationship("itemInfo")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Review(db.Model):
    __tablename__ = "review"

    uid = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"), nullable=False, primary_key=True)
    items = db.relationship("itemInfo")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class WishList(db.Model):
    __tablename__ = "wishList"

    uid = db.Column(db.Integer, db.ForeignKey(BuyerModel.uid), nullable=False, primary_key=True)
    items = db.relationship("itemInfo")

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
    seller_id = db.Column(db.Integer, db.ForeignKey("sellerInfo.uid"), nullable=False)

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
