"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""
from datetime import datetime
import os
import tempfile
from app import config, mail
from flask import request, jsonify, abort, render_template
from flask_restplus import Resource, fields
from flask_mail import Message
import boto3
import boto3.s3
from flask_jwt_extended import (jwt_required, create_access_token,
                                jwt_refresh_token_required, create_refresh_token,
                                get_jwt_identity, set_access_cookies,
                                set_refresh_cookies, get_raw_jwt, unset_access_cookies,
                                unset_refresh_cookies, get_jwt_claims)

from app import jwt
from .security import generate_encoded_token, decode_token, admin_required
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
            abort(400, "Invalid username or email.")

        if UserAuthModel.find_by_username(username):
            abort(400, "User name {} is already taken.".format(username))

        if UserAuthModel.find_by_useremail(email):
            abort(400, "Email {} is already used for another user".format(email))

        new_user = UserAuthModel(username=username, useremail=email, password=password)

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=username, user_claims={'role': new_user.role.value})
            refresh_token = create_refresh_token(identity=username)
            resp = jsonify({
                "success": True,
                "id": new_user.uid,
                "username": new_user.username,
                "email": new_user.useremail,
                "role": new_user.role.value})
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
            access_token = create_access_token(identity=username, user_claims={'role': current_user.role.value})
            refresh_token = create_refresh_token(identity=username)
            resp = jsonify({
                "success": True,
                "id": current_user.uid,
                "username": current_user.username,
                "email": current_user.useremail,
                "role": current_user.role.value})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)

            return resp
        abort(404, "Password for user {} is not correct".format(username))


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
        user = UserAuthModel.find_by_username(current_user)
        access_token = create_access_token(identity=current_user, user_claims={'role': user.role.value})

        resp = jsonify(success=True)
        set_access_cookies(resp, access_token)
        return resp


@authentication.route('/password/forget', doc={"description": "This route will send an email to the validated email address with a link to rest password, part of the link is jwt token"})
class ForgetPassword(Resource):
    @resource.doc(params={'email': "email for the new user, will return 404 if it doesn't exist in database."})
    def post(self):
        email = request.args['email']
        user = UserAuthModel.find_by_useremail(email)
        if user is None:
            abort(404, "We weren't able to identify you given the email provided.")
        payload = {"username": user.username, "useremail": user.useremail}
        encoded_token = generate_encoded_token(payload, 'secret', algorithm='HS256')
        # print(encoded_token)
        password_reset_url = 'https://thestars354.herokuapp.com/#/changePassword/'+encoded_token.decode("utf-8")+'/'+user.username
        msg = Message("Reset password - 354TheStars.com",
                      recipients=[email])
        msg.html = render_template('ResetPasswordEmail.html', username=user.username, link=password_reset_url)
        mail.send(msg)
        return jsonify(success=True)


@authentication.route('/changePassword/<string:token>', doc={"description": "This route will check the token in url, return success if validated."})
class CheckTokenInEmail(Resource):
    def get(self, token):
        # TODO: validate the token, then redirect to the reset password page.
        decoded_payload = decode_token(token, 'secret', algorithm=['HS256'])
        username = decoded_payload['username']
        email = decoded_payload['useremail']

        current_user = UserAuthModel.find_by_username(username)
        if not current_user:
            abort(404, "User with username {} not found".format(username))
        if current_user.useremail != email:
            abort(404, "Invalid token.")
        return jsonify(success=True)


@authentication.route('/changePassword', doc={"description": "This route will update the password for a user"})
class ResetPassword(Resource):
    @resource.doc(params={'username': "username for the account, will return 404 if it doesn't exist in database.",
                          'password': "new password for the user"})
    def put(self):
        username = request.args['username']
        password = request.args['password']
        current_user = UserAuthModel.find_by_username(username)
        if not current_user:
            abort(404, "User with username {} not found".format(username))
        current_user.password = password
        db.session.commit()
        return jsonify(success=True)


@authentication.route('/allUser', doc={"description": "Get the all users info in db, needs admin status"})
class AllUserInfo(Resource):
    @admin_required
    def get(self):
        users = UserAuthModel.query.all()
        return [i.serialize for i in users]


@authentication.route('/deleteUser/<string:username>', doc={"description": "This route will delete a user from the datebase, admin status needed"})
class DeleteUser(Resource):
    @admin_required
    def delete(self, username):
        user = UserAuthModel.find_by_username(username)
        if user is None:
            abort(404, "User with username {} not found".format(username))
        uid = user.uid
        buyer_info = BuyerModel.find_by_uid(uid)
        seller_info = SellerModel.find_by_uid(uid)
        if buyer_info is None or seller_info is None:
            abort(404, "Seller info or buyer info with uid {} not found".format(uid))
        orders = Order.find_by_buyer_id(buyer_info.uid)
        # clean up the database that relate to the user's buyer status
        db.session.query(wishListItem).\
            filter_by(buyer_id=buyer_info.uid).delete(synchronize_session=False)
        db.session.query(shoppingListItem). \
            filter_by(buyer_id=buyer_info.uid).delete(synchronize_session=False)
        for order in orders:
            db.session.query(orderItem).\
                filter_by(order_id=order.order_id).delete(synchronize_session=False)
            db.session.query(orderSeller).\
                filter_by(order_id=order.order_id).delete(synchronize_session=False)
        db.session.query(Review).\
            filter_by(buyer_id=buyer_info.uid).update({"buyer_id": None}, synchronize_session=False)

        # clean up the database that relate to the user's seller status
        db.session.query(orderSeller). \
            filter_by(seller_id=seller_info.uid).update({"seller_id": None}, synchronize_session=False)
        db.session.query(Item).\
            filter_by(seller_id=seller_info.uid).update({"seller_id": None}, synchronize_session=False)

        db.session.query(Order). \
            filter_by(buyer_id=buyer_info.uid).delete(synchronize_session=False)
        db.session.query(BuyerModel). \
            filter_by(uid=uid).delete(synchronize_session=False)
        db.session.query(SellerModel). \
            filter_by(uid=uid).delete(synchronize_session=False)
        db.session.delete(user)
        db.session.commit()
        return jsonify(success=True)


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


@resource.route('/updateAddress/<int:uid>/<int:address_index>', doc={"description": "Update the i-th address of the user."})
@resource.doc(params={'newAddress': "new address for the i-th address"})
class UpdateAddress(Resource):
    @jwt_required
    def put(self, uid, address_index):
        address = 'address'+str(address_index)

        db.session.query(BuyerModel) \
            .filter(BuyerModel.uid == uid). \
            update({address: request.args.get('newAddress')})

        db.session.commit()
        return jsonify(success=True)


@resource.route('/updatePaypal/<int:uid>', doc={"description": "Update user's paypal account"})
@resource.doc(params={'paypal': "new paypal account"})
class UpdatePaypal(Resource):
    @jwt_required
    def put(self, uid):
        db.session.query(BuyerModel) \
            .filter(BuyerModel.uid == uid). \
            update({"paypal": request.args.get('paypal')})

        db.session.commit()
        return jsonify(success=True)


@resource.route('/sellerInfo', doc={
    "description": "Search and return seller data that match the queried user uid"})
@resource.doc(params={'uid': "uid of the seller"})
class SellerInfo(Resource):
    def get(self):
        uid = request.args.get('uid')

        sellerInfo = SellerModel.find_by_uid(uid)
        if sellerInfo is None:
            abort(404, "Seller info for id {} not found".format(uid))
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
        payload = add_avg_rating(data)
        return jsonify(payload)


@resource.route('/category', doc={"description": "Get all items in a certain category"})
@resource.doc(params={
    'category': "Category query, one of {'Health & Beauty', 'Jewellery & Watches', 'Automotives & Electronics', 'Clothing, Shoes & Accessories', 'Books', 'Home Supplies'}"})
class Category(Resource):
    def get(self):
        query = request.args.get('category')
        data = Item.query.filter(Item.category == query).all()
        payload = add_avg_rating(data)
        return jsonify(payload)


@resource.route('/subcategory', doc={"description": "Get all items in a certain subcategory"})
@resource.doc(params={
    'subcategory': "Subcategory query, one of {'Men's Clothing', 'Children's Clothing', 'Pet Supplies', 'Women's Clothing', 'Cameras & Video Games', 'Women's Jewellery & Watches', 'Appliances', 'Creams', 'Garden Supplies', 'Shoes', 'Furniture & Accessories', 'Motos & Car Supplies', 'Men's Jewellery & Watches', 'Makeup', 'Books', 'Bags & Accessories', 'Sports', 'Cellphones, Computers & Tablets'}"})
class Subcategory(Resource):
    def get(self):
        query = request.args.get('subcategory').replace("’", "'")
        data = Item.query.filter(Item.subcategory == query).all()
        payload = add_avg_rating(data)
        return jsonify(payload)


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
        seller_auth_info = UserAuthModel.query.filter_by(uid=item.seller_id).first()
        reviews = [i.serialize for i in Review.query.filter(Review.item_id == item_id).all()]
        ratings = list(map(lambda x: x["rating"], reviews))
        ratings_avg = sum(ratings) / len(ratings) if len(ratings) != 0 else None
        item = item.serialize
        item.update({"rating": ratings_avg})
        result = {"seller_name": seller_auth_info.username if seller_auth_info is not None else None,
                  "item_info": item,
                  "reviews": reviews}
        return result

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
        payload = add_avg_rating(items)

        return jsonify(payload)


@resource.route('/item/deals', doc={"description": "Return top 20 most discounted items"})
class Deals(Resource):
    def get(self):
        items = Item.query.order_by(Item.discount.desc()).limit(20).all()
        payload = add_avg_rating(items)

        return jsonify(payload)


@resource.route('/review/<int:item_id>', doc={"description": "1. post a new review for an item. 2. Delete all reviews for an item."})
class CreateAndDeleteReview(Resource):
    @resource.doc(params={'content': "content of the review", 'rating': "rating"},)
    @jwt_required
    def post(self, item_id):
        item = Item.find_by_id(item_id)
        if item is None:
            abort(404, "Item with id {} not found".format(item_id))

        orders = Order.query.join(orderItem.join(Item, Item.item_id == item_id))
        if orders.count() == 0:
            abort(404, "No order record for item with id {} ".format(item_id))

        current_user_id = UserAuthModel.find_by_username(get_jwt_identity()).uid
        current_user_is_buyer = False

        for order in orders:
            if order.buyer_id == current_user_id:
                current_user_is_buyer = True
                break

        if not current_user_is_buyer:
            abort(400, "Current user {} is not a buyer of this item".format(current_user_id))

        image_keys = ['image1', 'image2', 'image3', 'image4', 'image5']
        images = []
        for image_key in image_keys:
            if request.files.get(image_key, False):
                images.append(request.files[image_key])
        image_url = ""
        image_prefix = "https://comp354.s3.us-east-2.amazonaws.com/reviewPic/"
        bucket_name = "comp354"
        s3 = boto3.client('s3',
                          aws_access_key_id=config.Config.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=config.Config.AWS_SECRET_ACCESS_KEY)
        with tempfile.TemporaryDirectory() as tempdir:
            for image in images:
                if image is not None:
                    # create a temporary folder to save the review images
                    image_path = os.path.join(tempdir, image.filename)
                    image.save(image_path)
                    s3.upload_file(image_path, bucket_name, 'reviewPic/{}'.format(image.filename), ExtraArgs={'ACL': 'public-read'})
                    image_url += image_prefix+image.filename+"&"
        content = request.args.get('content')
        rating = request.args.get('rating')

        new_review = Review(buyer_id=current_user_id, item_id=item_id, content=content, rating=rating, images=image_url)
        item.reviews.append(new_review)
        db.session.commit()
        return jsonify(success=True)

    @jwt_required
    def delete(self, item_id):
        item = Item.query.filter(Item.item_id == item_id).first()
        if item is None:
            abort(404, "Item with id {} not found".format(item_id))
        reviews = db.session.query(Review).filter_by(item_id=item_id)
        reviews.delete(synchronize_session=False)
        db.session.commit()
        return jsonify(success=True)

@resource.route('/review/<int:item_id>/<int:review_id>', doc={"description": "Manipulate (put, delete) a review for an item."})
class PutAndDeleteReview(Resource):
    @resource.doc(params={'response': "seller's response for the review"})
    @jwt_required
    def put(self, item_id, review_id):
        db.session.query(Review)\
            .filter(Review.review_id == review_id and Review.item_id == item_id).\
            update({"reply": request.args.get('response')})
        db.session.commit()
        return jsonify(success=True)

    @jwt_required
    def delete(self, item_id, review_id):
        review = db.session.query(Review) \
            .filter(Review.review_id == review_id and Review.item_id == item_id)
        if review is None:
            abort(404, "Review with id {} not found".format(review_id) + "for item {}".format(item_id))
        review.delete(synchronize_session=False)
        db.session.commit()
        return jsonify(success=True)


@resource.route('/shopping-cart/<int:user_id>', doc={"description": "Get and empty items in the shopping cart"})
class ShoppingCart(Resource):
    def get(self, user_id):
        shoppingListItems = db.session.query(shoppingListItem).filter_by(buyer_id=user_id).all()
        shopping_list_items = []
        for i in shoppingListItems:
            item = Item.query.filter_by(item_id=i.item_id).first()
            shopping_list_items.append({"item": item.serialize,
                                        "qty": i.quantity})

        return shopping_list_items

    def delete(self, user_id):
        db.engine.execute(db.delete(shoppingListItem)
                          .where(shoppingListItem.c.buyer_id == user_id))
        return jsonify(success=True)


@resource.route('/shopping-cart/<int:user_id>/<int:item_id>',
                doc={"description": "Add and remove items in the shopping cart"})
class ShoppingCart(Resource):
    @resource.doc(params={'newQuantity': "new quantity"},)
    def post(self, user_id, item_id):
        buyer = BuyerModel.find_by_uid(user_id)
        item = Item.query.filter_by(item_id=item_id).first()
        qty = int(request.args.get('newQuantity'))
        if item is None:
            abort(404, "Item with id {} not found".format(item_id))
        if buyer is None:
            abort(404, "Buyer with id {} not found".format(user_id))
        if not buyer.add_to_shopping_list(item, qty):
            abort(404, "Trying to remove more items than the quantity in cart.")
        return jsonify(success=True)

    def delete(self, user_id, item_id):
        items = db.session.query(shoppingListItem).filter_by(buyer_id=user_id, item_id=item_id)
        if items.count() == 0:
            abort(404, "Item with id {} not in the shopping cart".format(item_id))
        items.delete(synchronize_session=False)
        db.session.commit()
        return jsonify(success=True)


def add_avg_rating(items):
    items = [i.serialize for i in items]
    reviews = [i.serialize for i in Review.query.all()]
    for item in items:
        rating = 0
        count = 0
        for review in reviews:
            if review["item_id"] == item["item_id"]:
                rating += review["rating"]
                count += 1
        item["rating"] = None if count == 0 else rating / count
    return items


@resource.route('/place-order/<int:user_id>/<int:item_id>', doc={"description": "Place order for a single item"})
class PlaceOrder(Resource):
    @jwt_required
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


@resource.route('/place-order-in-shopping-cart/<int:user_id>/<int:buyer_address_index>/<string:shipping_method>',
                doc={"description": "Place order for entire shopping cart"})
class PlaceOrderInShoppingCart(Resource):
    @jwt_required
    def post(self, user_id, buyer_address_index, shipping_method):
        buyer = BuyerModel.query.filter_by(uid=user_id).first()
        order = Order(buyer_id=buyer.uid, purchase_date=db.func.current_date(), buyer_address_index=buyer_address_index, shipping_method=shipping_method)
        shoppingListItems = db.session.query(shoppingListItem).filter_by(buyer_id=user_id).all()

        if buyer is None:
            abort(404, "Buyer with id {} not found".format(user_id))

        order.save_to_db()

        for shopping_list_item in shoppingListItems:
            item = Item.query.filter_by(item_id=shopping_list_item.item_id).first()
            if item is None:
                abort(404, "Item with id {} not found".format(item.item_id))
            elif item.quantity - item.quantity_sold <= 0:
                abort(403, "Not enough stock for item {} (1)".format(item.item_id))
            seller = SellerModel.query.filter_by(uid=item.seller_id).first()
            if seller is not None:
                seller.add_commission(item)
            order.add_item(item)
            new_quantity_sold = item.quantity_sold + shopping_list_item.quantity
            if item.quantity - new_quantity_sold < 0:
                abort(403, "Not enough stock for item {} (2)".format(item.item_id))
            item.quantity_sold += shopping_list_item.quantity
            db.session.query(orderItem). \
                filter_by(order_id=order.order_id, item_id=item.item_id).update({"order_item_quantity": shopping_list_item.quantity}, synchronize_session=False)

            list_item = db.session.query(shoppingListItem).filter_by(buyer_id=user_id, item_id=item.item_id)
            list_item.delete(synchronize_session=False)
            db.session.commit()
        return jsonify(order.serialize)


@resource.route('/wish-list/<int:user_id>/<int:item_id>',doc={"description": "Add and remove wish list"})
class WishList(Resource):
    def post(self, user_id, item_id):
        buyer = BuyerModel.query.filter_by(uid=user_id).first()
        item = Item.query.filter_by(item_id=item_id).first()
        if item is None:
            abort(404, "Item with id {} not found".format(item_id))
        elif buyer is None:
            abort(404, "Buyer with id {} not found".format(user_id))
        buyer.add_to_wish_list(item)
        return jsonify(success=True)

    def delete(self, user_id, item_id):
        item = db.session.query(wishListItem).filter_by(buyer_id=user_id, item_id=item_id)
        if item.count() == 0:
            abort(404, "Item with id {} not in the shopping cart".format(item_id))
        item.delete(synchronize_session=False)
        db.session.commit()
        return jsonify(success=True)

    def get(self, user_id, item_id):
        item = Item.find_by_id(item_id)
        buyer = BuyerModel.find_by_uid(user_id)
        if item is None:
            abort(404, "Item with id {} not found".format(item_id))
        elif buyer is None:
            abort(404, "Buyer with id {} not found".format(user_id))
        wish_list_item = db.session.query(wishListItem).filter_by(buyer_id=user_id, item_id=item_id)
        if wish_list_item.count() == 0:
            return jsonify(False)
        return jsonify(True)


@resource.route('/wish-list/<int:user_id>',doc={"description": "Get wish list"})
class WishList(Resource):
    def get(self, user_id):
        items = db.session.query(wishListItem).filter_by(buyer_id=user_id).all()
        return jsonify([Item.query.filter_by(item_id=i.item_id).first().serialize for i in items])


@resource.route('/orders/<start_date>/<end_date>',
                doc={"description": "Return all orders during a given period of time"})
class AllOrders(Resource):
    def get(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            if start > end:
                abort(400, "Invalid Date")
        except:
            abort(400, "Invalid Date")
        orders = Order.query.filter(start <= Order.purchase_date, end >= Order.purchase_date).all()
        return jsonify([i.serialize for i in orders])


@resource.route('/commission/<start_date>/<end_date>',
                doc={"description": "Return total commission during a given period of time"})
class TotalCommission(Resource):
    def get(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            if start > end:
                abort(400, "Invalid Date")
        except:
            abort(400, "Invalid Date")
        commission = 0
        for seller in SellerModel.query.all():
            seller_orders = db.session.query(orderSeller).filter_by(seller_id=seller.uid).all()
            orders = [Order.query.filter_by(order_id=i.order_id).order_by(Order.purchase_date.asc()).first() for i in seller_orders]
            counter = 0
            for order in orders:
                order_items = db.session.query(orderItem).filter_by(order_id=order.order_id).all()
                items = [Item.query.filter_by(item_id=i.item_id, seller_id=seller.uid).first() for i in order_items]
                for item in items:
                    if item is not None:
                        counter += 1
                        if order.purchase_date <= end and order.purchase_date >= start:
                            if counter < 10:
                                commission += item.price * (1 - item.discount) * 0.03
                            else:
                                commission += item.price * (1 - item.discount) * 0.08
        return jsonify(commission)
