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
            "images": self.images
        }
