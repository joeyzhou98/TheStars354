import json
import random
from app.api.models import *
from app import db

db.create_all()

# Check that there are users, sellers and buyers in database
if UserAuthModel.query.count() == 0:
    raise Exception("No UserAuthModel instances in database, please add more and try again")
if SellerModel.query.count() == 0:
    raise Exception("No SellerModel instances in database, please add more and try again")
if BuyerModel.query.count() == 0:
    raise Exception("No BuyerModel instances in database, please add more and try again")

# Check if database already has items and if not, create items
if Item.query.count() == 0:

    # Get sellers
    sellers = [i.serialize for i in SellerModel.query.all()]

    # Load items
    with open("items.json", "r") as f:
        items = json.load(f)

    # Populate items in database
    for item in items:
        quantity = random.randrange(9) + 1
        db.session.add(Item(item_name=item["name"],
                            price=item["price"],
                            category=item["category"],
                            subcategory=item["subcategory"],
                            brand=item["brand"],
                            description=item["description"],
                            quantity=quantity,
                            quantity_sold=random.randrange(quantity),
                            discount=random.uniform(0.1, 0.7) if random.uniform(0, 1) < 0.5 else 0.0,
                            images="https://comp354.s3.us-east-2.amazonaws.com/itemPic/" + item["picture"],
                            seller_id=random.choice(sellers)["uid"]))

    # Commit session
    db.session.commit()

# Create random reviews if no reviews
if Review.query.count() == 0:

    # Get buyers
    buyers = [i.serialize for i in BuyerModel.query.all()]

    # Get items
    items = [i.serialize for i in Item.query.all()]

    # Load random reviews
    with open("reviews.json", "r") as f:
        reviews = json.load(f)

    for item in items:
        # Choose the number of reviews between 0 and the quantity sold
        n = random.randint(0, item["quantity_sold"])

        # Create the number of reviews associated with that item with a random review
        for i in range(n):
            review = random.choice(reviews)
            db.session.add(Review(buyer_id=random.choice(buyers)["uid"],
                                  item_id=item["item_id"],
                                  rating=review["rating"],
                                  content=review["message"]))

    # Commit session
    db.session.commit()
