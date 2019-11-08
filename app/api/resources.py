"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request, redirect, jsonify, abort
from flask_restplus import Resource, fields
from flask_jwt_extended import (jwt_required, create_access_token,
                                jwt_refresh_token_required, create_refresh_token,
                                get_jwt_identity, set_access_cookies,
                                set_refresh_cookies, get_raw_jwt, unset_access_cookies,
                                unset_refresh_cookies)

from app import jwt
from .security import require_auth
from . import api_rest
from .models import *

resource = api_rest.namespace('resource', description='Resource namespace')
authentication = api_rest.namespace('authentication', description='Authentication namespace')


# class SecureResource(Resource):
#    """ Calls require_auth decorator on all requests """
#    method_decorators = [require_auth]

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_in_blacklist(jti)


@authentication.route('/registration', doc={
    "description": "Registration route, will store an access token and a refresh token in cookies if registration is successful"})
@resource.doc(params={'username': "user name for the new user, will return 400 it already exists in database.",
                      'email': "email for the new user, will return 400 if it already exists in database.",
                      'password': "MD5 hashed password for the new user."})
class UserRegistration(Resource):
    def post(self):
        username = request.args['username']
        email = request.args['email']
        password = request.args['password']


        if username is None or email is None or password is None:
            abort(400)  # missing arguments

        if UserAuthModel.find_by_username(username):
            abort(400, "User with username {} aleady exists in db.".format(username))  # existing user

        if UserAuthModel.find_by_useremail(email):
            abort(400, "User with email {} aleady exists in db.".format(email))  # existing email

        new_user = UserAuthModel(username=username, useremail=email, password=password)

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            resp = jsonify(success=True)
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
        except:
            return jsonify(success=False), 500


@authentication.route('/login', doc={
    "description": "Login route, will store an access token and a refresh token in the cookies if login is successful"})
@resource.doc(params={'username': "user name of the user, will return 404 if it doesn't exist in database.",
                      'password': "MD5 hashed password of the user, will return 404 if it doesn't match with the password stored in db."})
class UserLogin(Resource):
    def post(self):
        username = request.args['username']
        password = request.args['password']
        current_user = UserAuthModel.find_by_username(username)

        if not current_user:
            abort(404, "User with username {} not found".format(username))

        if current_user.password == password:
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            resp = jsonify(success=True)
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
        abort(404, "Credential info for user {} is not correct".format(username))


@authentication.route('/logout/access', doc={
    "description": "access token logout route, will put access token into token blacklist if successfully executed, access token needed."})
class LogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            resp = jsonify(success=True)
            unset_access_cookies(resp)
            return resp
        except:
            return jsonify(success=False), 500


@authentication.route('/logout/refresh', doc={
    "description": "refresh token logout route, will put refresh token into token blacklist if successfully executed, refresh token needed."})
class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            resp = jsonify(success=True)
            unset_refresh_cookies(resp)
            return resp
        except:
            return jsonify(success=False), 500


@authentication.route('/token/refresh', doc={
    "description": "access token refresh route, will generate a new access token for the user, refresh token needed."})
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        resp = jsonify(success=True)
        set_access_cookies(resp, access_token)
        return resp


@authentication.route('/password/reset')
class ResetPassword(Resource):
    @jwt_required
    def get(self):
        return {'message': 'Hit the user password reset endpoint.'}


@resource.route('/buyerInfo', doc={
    "description": "Search and return buyer data that match the queried user name, access token needed"})
@resource.doc(params={'username': "user name of the user"})
class BuyerInfo(Resource):
    @jwt_required
    def get(self):
        username = request.args.get('username')
        current_user = UserAuthModel.find_by_username(username)
        if not current_user:
            return jsonify(success=False)

        buyerInfo = BuyerModel.find_by_uid(current_user.uid)
        if buyerInfo is None:
            abort(404, "Buyer info for user {} not found".format(username))
        return jsonify(buyerInfo.serialize)


@resource.route('/sellerInfo', doc={
    "description": "Search and return seller data that match the queried user name, access token needed"})
@resource.doc(params={'username': "user name of the user"})
class SellerInfo(Resource):
    @jwt_required
    def get(self):
        username = request.args.get('username')
        current_user = UserAuthModel.find_by_username(username)
        if not current_user:
            return jsonify(success=False)

        sellerInfo = SellerModel.find_by_uid(current_user.uid)
        if sellerInfo is None:
            abort(404, "Seller info for user {} not found".format(username))
        return jsonify(sellerInfo.serialize)


@resource.route('/search', doc={
    "description": "Search and return items that match the search query string, returns all items if search query is empty"})
@resource.doc(params={'query': 'Search query'})
class Search(Resource):
    def get(self):
        query = request.args.get('query')
        if query is not None:
            query = "%{}%".format(query)
            data = Item.query.filter((
                    Item.description.like(query) |
                    Item.item_name.like(query) |
                    Item.brand.like(query)
            )).all()
        else:
            data = Item.query.all()
        return jsonify([i.serialize for i in data])


@resource.route('/category', doc={"description": "Get all items in a certain category"})
@resource.doc(params={
    'category': "Category query, one of {'Health & Beauty', 'Jewellery & Watches', 'Automotives & Electronics', 'Clothing, Shoes & Accessories', 'Books', 'Home Supplies'}"})
class Category(Resource):
    def get(self):
        query = request.args.get('category')
        data = Item.query.filter(Item.category == query).all()
        return jsonify([i.serialize for i in data])


@resource.route('/subcategory', doc={"description": "Get all items in a certain subcategory"})
@resource.doc(params={
    'subcategory': "Subcategory query, one of {'Men's Clothing', 'Children's Clothing', 'Pet Supplies', 'Women's Clothing', 'Cameras & Video Games', 'Women's Jewellery & Watches', 'Appliances', 'Creams', 'Garden Supplies', 'Shoes', 'Furniture & Accessories', 'Motos & Car Supplies', 'Men's Jewellery & Watches', 'Makeup', 'Books', 'Bags & Accessories', 'Sports', 'Cellphones, Computers & Tablets'}"})
class Subcategory(Resource):
    def get(self):
        query = request.args.get('subcategory').replace("’", "'")
        data = Item.query.filter(Item.subcategory == query).all()
        return jsonify([i.serialize for i in data])


create_item_payload = api_rest.model('ItemModel', {
    'item_name': fields.String(description='Item name', required=True),
    'price': fields.Float(description='Item price', min=0.05, required=True),
    'category': fields.String(description='Item category', required=True),
    'subcategory': fields.String(description='Item subcategory', required=True),
    'brand': fields.String(description='Item brand', required=True),
    'description': fields.String(description='Item description, maximum 1000 characters', required=True),
    'quantity': fields.Integer(description='Number of items in stock', min=1, required=True),
    'discount': fields.Float(description='Discount on the price', min=0.0, max=1.0, required=True),
    'images': fields.String(description='Comma separated item image urls', required=True)
})
item_keys = ("item_name", "price", "category", "subcategory", "brand", "description", "quantity", "discount", "images")


@resource.route('/item/<int:item_id>', doc={"description": "Manipulate (get, update or delete) a specific item"})
class ItemRoutes(Resource):
    def get(self, item_id):
        item = Item.query.filter(Item.item_id == item_id).first()
        if item is None:
            abort(404, "Item with id {} not found".format(item_id))
        return jsonify(item.serialize)

    @resource.expect(create_item_payload)
    @jwt_required
    def put(self, item_id):
        item = Item.query.filter(Item.item_id == item_id).first()
        payload = request.json

        if item is None:
            abort(404, "Item with id {} not found".format(item_id))
        if not all(k in payload.keys() for k in item_keys):
            abort(400, "Missing attribute in payload")

        item.item_name = payload["item_name"]
        item.price = payload["price"]
        item.category = payload["category"]
        item.subcategory = payload["subcategory"]
        item.brand = payload["brand"]
        item.description = payload["description"]
        item.quantity = payload["quantity"]
        item.discount = payload["discount"]
        item.images = payload["images"]

        try:
            db.session.commit()
        except Exception as e:
            abort(400, str(e))

        return jsonify(success=True)

    @jwt_required
    def delete(self, item_id):
        item = Item.query.filter(Item.item_id == item_id)
        if item is not None:
            item.delete()
            db.session.commit()
            return jsonify(success=True)
        else:
            abort(404, "Sorry, item with id {} not found".format(item_id))


@resource.route('/item', doc={"description": "Create new item to be inserted into database"})
@resource.expect(create_item_payload)
class CreateItem(Resource):
    @jwt_required
    def post(self):
        payload = request.json
        try:
            db.session.add(Item(item_name=payload["item_name"],
                                price=payload["price"],
                                category=payload["category"],
                                subcategory=payload["subcategory"],
                                brand=payload["brand"],
                                description=payload["description"],
                                quantity=payload["quantity"],
                                discount=payload["discount"],
                                images=payload["images"]))
        except KeyError as e:
            abort(400, "Missing attribute " + str(e))
        try:
            db.session.commit()
        except Exception as e:
            abort(400, str(e))
        return jsonify(success=True)


@resource.route('/item/best', doc={"description": "Return top 20 most sold items"})
class BestSellers(Resource):
    def get(self):
        items = Item.query.order_by(Item.quantity_sold.desc()).limit(20).all()
        return jsonify([i.serialize for i in items])


@resource.route('/item/deals', doc={"description": "Return top 20 most discounted items"})
class Deals(Resource):
    def get(self):
        items = Item.query.order_by(Item.discount.desc()).limit(20).all()
        return jsonify([i.serialize for i in items])


@resource.route('/shopping-cart/<int:user_id>', doc={"description": "Get and empty items in the shopping cart"})
class ShoppingCart(Resource):
    def get(self, user_id):
        items = db.engine.execute(
            db.select([Item.item_id, Item.item_name, Item.price, shoppingListItem.c.quantity]).
            where(shoppingListItem.c.item_id == Item.item_id and shoppingListItem.c.buyer_id == user_id)
        )
        return jsonify([{
            "item_id": i.item_id,
            "name": i.item_name,
            "price": i.price,
            "quantity": i.quantity,
        }for i in items])

    def delete(self, user_id):
        db.engine.execute(db.delete(shoppingListItem)
                          .where(shoppingListItem.c.buyer_id == user_id))
        return jsonify(success=True)


@resource.route('/shopping-cart/<int:user_id>/<int:item_id>', doc={"description": "Add and remove items in the shopping cart"})
class ShoppingCart(Resource):
    def post(self, user_id, item_id):
        buyer = BuyerModel.query.filter_by(uid=user_id).first()
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            abort(404, "Item with id {} not found".format(item_id))
        elif buyer is None:
            abort(404, "Buyer with id {} not found".format(user_id))
        buyer.add_to_shopping_list(item)
        return jsonify(success=True)

    def delete(self, user_id, item_id):
        items = db.session.query(shoppingListItem).filter_by(buyer_id=user_id, item_id=item_id)
        if items.count() == 0:
            abort(404, "Item with id {} not in the shopping cart".format(item_id))
        items.delete(synchronize_session=False)
        db.session.commit()
        return jsonify(success=True)


@resource.route('/place-order/<int:user_id>/<int:item_id>', doc={"description": "Place order for a single item"})
class PlaceOrder(Resource):
    def post(self, user_id, item_id):
        buyer = BuyerModel.query.filter_by(uid=user_id).first()
        item = Item.query.filter_by(item_id=item_id).first()

        if item is None:
            abort(404, "Item with id {} not found".format(item_id))
        elif item.quantity - item.quantity_sold <= 0:
            abort(403, "Not enough stock for item {}".format(item_id))
        elif buyer is None:
            abort(404, "Buyer with id {} not found".format(user_id))

        seller = SellerModel.query.filter_by(uid=item.seller_id).first()
        if seller is not None:
            seller.add_commission(item)

        order = Order(buyer_id=buyer.uid, purchase_date=db.func.current_date())
        order.save_to_db()
        order.add_item(item)
        item.quantity_sold += 1
        db.session.commit()
        return jsonify(success=True)


@resource.route('/place-order-in-shopping-cart/<int:user_id>', doc={"description": "Place order for entire shopping cart"})
class PlaceOrderInShoppingCart(Resource):
    def post(self, user_id):
        buyer = BuyerModel.query.filter_by(uid=user_id).first()
        order = Order(buyer_id=buyer.uid, purchase_date=db.func.current_date())
        items = Item.query.join(shoppingListItem.join(BuyerModel, BuyerModel.uid == user_id))

        if buyer is None:
            abort(404, "Buyer with id {} not found".format(user_id))
        for item in items:
            if item is None:
                abort(404, "Item with id {} not found".format(item.item_id))
            elif item.quantity - item.quantity_sold <= 0:
                abort(403, "Not enough stock for item {}".format(item.item_id))

        order.save_to_db()
        for item in items:
            seller = SellerModel.query.filter_by(uid=item.seller_id).first()
            if seller is not None:
                seller.add_commission(item)
            order.add_item(item)
            item.quantity_sold += 1
            list_item = db.session.query(shoppingListItem).filter_by(buyer_id=user_id, item_id=item.item_id)
            list_item.delete(synchronize_session=False)
            db.session.commit()

        return jsonify(success=True)

