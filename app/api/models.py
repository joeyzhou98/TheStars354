from app import db
import enum


class Roles(str, enum.Enum):
    ADMIN = 'admin'
    NORMAL = 'normal'


class ShippingMethod(str, enum.Enum):
    REGULAR = 'regular'
    EXPRESS = 'express'


orderItem = db.Table(
    "orderItem",
    db.Column('order_id', db.Integer, db.ForeignKey("order.order_id")),
    db.Column("item_id", db.Integer, db.ForeignKey("item.item_id")),
    db.Column("order_item_quantity", db.Integer, default=1)
)

wishListItem = db.Table(
    "wishListItem",
    db.Column('buyer_id', db.Integer, db.ForeignKey("buyerInfo.uid")),
    db.Column("item_id", db.Integer, db.ForeignKey("item.item_id"))
)

shoppingListItem = db.Table(
    "shoppingListItem",
    db.Column('buyer_id', db.Integer, db.ForeignKey("buyerInfo.uid")),
    db.Column("item_id", db.Integer, db.ForeignKey("item.item_id")),
    db.Column("quantity", db.Integer, default=1)
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
    role = db.Column(db.Enum(Roles), nullable=False, default=Roles.NORMAL.value, server_default=Roles.NORMAL.value)

    @property
    def serialize(self):
        return {
            "uid": self.uid,
            "username": self.username,
            "useremail": self.useremail,
            "role": self.role}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        buyer = BuyerModel(uid=self.uid)
        seller = SellerModel(uid=self.uid, membership_date=db.func.current_date())
        db.session.add(buyer)
        db.session.add(seller)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_useremail(cls, email):
        return cls.query.filter_by(useremail=email).first()

    @classmethod
    def find_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid).first()


class RevokedTokenModel(db.Model):
    __tablename__ = 'revokedTokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_in_blacklist(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


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

    @property
    def serialize(self):
        orders = Order.query.filter_by(buyer_id=self.uid).all()
        wishlists = db.session.query(wishListItem).filter_by(buyer_id=self.uid).all()
        wish_list_items = [Item.query.filter_by(item_id=i.item_id).first() for i in wishlists]
        shoppingListItems = db.session.query(shoppingListItem).filter_by(buyer_id=self.uid).all()
        shopping_list_items = []
        for i in shoppingListItems:
            item = Item.query.filter_by(item_id=i.item_id).first()
            shopping_list_items.append({"item": item.serialize,
                                       "quantity": i.quantity})

        reviews = Review.query.filter_by(buyer_id=self.uid).all()
        return {
            "uid": self.uid,
            "address1": self.address1,
            "address2": self.address2,
            "address3": self.address3,
            "paypal": self.paypal,
            "order_history": [order.serialize for order in orders],
            "wish_list": [i.serialize for i in wish_list_items],
            "shopping_list": shopping_list_items,
            "review_list": [review.serialize for review in reviews]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def add_to_wish_list(self, item):
        self.wish_list.append(item)
        db.session.commit()

    def add_to_shopping_list(self, item, qty):
        list_item = db.session.query(shoppingListItem).filter_by(buyer_id=self.uid, item_id=item.item_id)
        if list_item.count() == 1:
            new_quantity = list_item.first().quantity + qty
            if new_quantity < 0:
                return False
            list_item.update({"quantity": new_quantity}, synchronize_session=False)
        elif list_item.count() == 0:
            self.shopping_list.append(item)
            if qty > 1:
                list_item.update({"quantity": qty}, synchronize_session=False)
        db.session.commit()
        return True

    def set_paypal(self, paypal):
        BuyerModel.query.filter_by(uid=self.uid).first().paypal = paypal
        db.session.commit()

    def get_address_from_index(self, index):
        if index == 1:
            return self.address1
        if index == 2:
            return self.address2
        if index == 3:
            return self.address3
        return None

    @classmethod
    def buyer_exists(cls, uid):
        if cls.query.filter_by(uid=uid).count() == 0:
            return False
        else:
            return True

    @classmethod
    def find_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid).first()


class SellerModel(db.Model):
    __tablename__ = "sellerInfo"

    uid = db.Column(db.Integer, db.ForeignKey(UserAuthModel.uid), primary_key=True)
    membership_date = db.Column(db.Date, nullable=False)
    total_commission = db.Column(db.Float, nullable=False, default=0.0)
    offered_products = db.relationship("Item")
    orders = db.relationship("Order", secondary=orderSeller)

    @property
    def serialize(self):
        order_sellers = db.session.query(orderSeller).distinct(Order.order_id).filter_by(seller_id=self.uid).all()
        orders = []
        for i in order_sellers:
            order = Order.query.filter_by(order_id=i.order_id).first()
            orders.append({"order": order.serialize})

        items = Item.query.filter_by(seller_id=self.uid).all()
        return {
            "uid": self.uid,
            "membership_date": self.membership_date,
            "total_commission": self.total_commission,
            "offered_products": [i.serialize for i in items],
            "orders": orders}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def add_offered_products(self, item):
        self.offered_products.append(item)
        db.session.commit()

    def add_commission(self, item):
        percentage = 0.08
        sold_quantity = 0
        sold_items = Item.query.filter_by(seller_id=self.uid)
        for sold_item in sold_items:
            sold_quantity += sold_item.quantity_sold
        if sold_quantity <= 10:
            percentage = 0.03
        self.total_commission += item.price * percentage

    @classmethod
    def get_offered_products(cls):
        return cls.query.join(SellerModel, Item)

    @classmethod
    def seller_exists(cls, seller_id):
        if cls.query.filter_by(uid=seller_id).count() == 0:
            return False
        else:
            return True

    @classmethod
    def find_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid).first()


class Order(db.Model):
    __tablename__ = "order"

    order_id = db.Column(db.Integer, primary_key=True, index=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey("buyerInfo.uid"), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    items = db.relationship("Item", secondary=orderItem)
    buyer_address_index = db.Column(db.Integer, nullable=False)
    shipping_method = db.Column(db.Enum(ShippingMethod), nullable=False)
    coupon_discount = db.Column(db.Float, nullable=False, default=0.0)

    @property
    def serialize(self):
        order_items = db.session.query(orderItem).filter_by(order_id=self.order_id).all()
        orders = []
        for i in order_items:
            item = Item.query.filter_by(item_id=i.item_id).first()
            if item is not None:
                orders.append({"item": item.serialize, "order_item_quantity": i.order_item_quantity})

        return {
            "order_id": self.order_id,
            "buyer_id": self.buyer_id,
            "purchase_date": self.purchase_date,
            "items": orders,
            "buyer_address_index": self.buyer_address_index,
            "shipping_method": self.shipping_method,
            "coupon_discount": self.coupon_discount}

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

    @classmethod
    def find_by_buyer_id(cls, buyer_id):
        return cls.query.filter_by(buyer_id=buyer_id).all()


class Review(db.Model):
    __tablename__ = "review"

    review_id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyerInfo.uid'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'))
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    reply = db.Column(db.String(512), nullable=True)  # Seller's reply to buyer's rating
    content = db.Column(db.String(512), nullable=True)
    images = db.Column(db.String(1000), nullable=True)

    @property
    def serialize(self):
        return {
            "review_id": self.review_id,
            "buyer_id": self.buyer_id,
            "item_id": self.item_id,
            "rating": self.rating,
            "reply": self.reply,
            "content": self.content,
            "images": self.images}

    def save_to_db(self):
        if BuyerModel.buyer_exists(self.buyer_id):
            print("No such buyer")
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
        reviews = [i.serialize for i in Review.query.filter(Review.item_id == self.item_id).all()]

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
            "seller_id": self.seller_id,
            "reviews": reviews
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

    @classmethod
    def find_by_id(cls, item_id):
        return cls.query.filter_by(item_id=item_id).first()


class Coupon(db.Model):
    __tablename__ = 'coupon'

    coupon_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(300), unique=True, nullable=False)
    discount = db.Column(db.Float, nullable=False, default=0.0)

    @property
    def serialize(self):
        return {
            "coupon_id": self.coupon_id,
            "code": self.code,
            "discount": self.discount}

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

