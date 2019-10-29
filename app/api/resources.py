"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request, redirect, jsonify, abort
from flask_restplus import Resource, fields

from .security import require_auth
from . import api_rest
from .models import *

resource = api_rest.namespace('resource', description='Resource namespace')
authentication = api_rest.namespace('authentication', description='Authentication namespace')


class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]


# @resource.route('/resource/<string:resource_id>')
# class ResourceOne(Resource):
#     """ Unsecure Resource Class: Inherit from Resource """
#
#     def get(self, resource_id):
#         timestamp = datetime.utcnow().isoformat()
#         return {'timestamp': timestamp}
#
#     def post(self, resource_id):
#         json_payload = request.json
#         return {'timestamp': json_payload}, 201
#
#
# @resource.route('/secure-resource/<string:resource_id>')
# class SecureResourceOne(SecureResource):
#     """ Secure Resource Class: Inherit from SecureResource """
#
#     def get(self, resource_id):
#         timestamp = datetime.utcnow().isoformat()
#         return {'timestamp': timestamp}


# TODO add logic after deciding the authentication method
@authentication.route('/registration/')
class UserRegistration(SecureResource):
    def get(self):
        return {'message': 'Hit the user registration endpoint, show the registration page.'}

    def post(self):
        username = request.args['username']
        email = request.args['email']
        password = request.args['password']

        if UserAuthModel.find_by_username(username):
            return {'message': 'User name exists.'}

        if UserAuthModel.find_by_useremail(email):
            return {'message': 'User email exists.'}

        new_user = UserAuthModel(username=username, useremail=email, password=password)
        new_user.save_to_db()
        timestamp = datetime.utcnow().isoformat()
        return {'message': 'saved to database', 'timestamp': timestamp}


# TODO add logic after deciding the authentication method
@authentication.route('/login/')
class UserLogin(SecureResource):
    def get(self):
        return {'message': 'Hit the user login endpoint with GET, show the login page'}

    def post(self):
        username = request.args['username']
        password = request.args['password']
        login = UserAuthModel.query.filter_by(username=username, password=password).first()
        if login is not None:
            return redirect('/')


@authentication.route('/logout/access')
class LogoutAccess(SecureResource):
    def post(self):
        return {'message': 'Hit the user logout access endpoint.'}


@authentication.route('/logout/refresh')
class LogoutRefresh(SecureResource):
    def post(self):
        return {'message': 'Hit the user logout refresh endpoint.'}


@authentication.route('/token/refresh')
class TokenRefresh(SecureResource):
    def post(self):
        return {'message': 'Hit the token refresh endpoint.'}


@authentication.route('/password/reset')
class ResetPassword(SecureResource):
    def post(self):
        return {'message': 'Hit the user password reset endpoint.'}


@resource.route('/search', doc={"description": "Search and return items that match the search query string, returns all items if search query is empty"})
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
@resource.doc(params={'category': "Category query, one of {'Health & Beauty', 'Jewellery & Watches', 'Automotives & Electronics', 'Clothing, Shoes & Accessories', 'Books', 'Home Supplies'}"})
class Category(Resource):
    def get(self):
        query = request.args.get('category')
        data = Item.query.filter(Item.category == query).all()
        return jsonify([i.serialize for i in data])


@resource.route('/subcategory', doc={"description": "Get all items in a certain subcategory"})
@resource.doc(params={'subcategory': "Subcategory query, one of {'Men's Clothing', 'Children's Clothing', 'Pet Supplies', 'Women's Clothing', 'Cameras & Video Games', 'Women's Jewellery & Watches', 'Appliances', 'Creams', 'Garden Supplies', 'Shoes', 'Furniture & Accessories', 'Motos & Car Supplies', 'Men's Jewellery & Watches', 'Makeup', 'Books', 'Bags & Accessories', 'Sports', 'Cellphones, Computers & Tablets'}"})
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
