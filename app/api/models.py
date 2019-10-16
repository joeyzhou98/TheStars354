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
        return cls.query.filter_by(category=category).first()

    @classmethod
    def find_by_brand(cls, brand):
        return cls.query.filter_by(brand=brand).first()

    @classmethod
    def find_by_price(cls, price):
        return cls.query.filter_by(price <= price).first()
