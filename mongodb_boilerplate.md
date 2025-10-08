# MongoDB — create DB, collections, unique index, seed data (do this now)
## Option A — Use mongosh (quick):

### Open a terminal and run:
```js
mongosh   # connects to local MongoDB


# Then run these commands:

use ecommerce

// create collections (optional, insert will create automatically)
db.createCollection("subscribers")
db.createCollection("products")
db.createCollection("categories")

// unique index for subscribers.email to avoid duplicates / race conditions
db.subscribers.createIndex({ email: 1 }, { unique: true })

// insert categories (example)
db.categories.insertMany([
  { id: 1, name: "T-Shirts", image: "/images/category-tshirts.jpg", count: 45 },
  { id: 2, name: "Jackets", image: "/images/category-jackets.jpg", count: 23 },
  { id: 3, name: "Dresses", image: "/images/category-dresses.jpg", count: 34 },
  { id: 4, name: "Pants", image: "/images/category-pants.jpg", count: 28 }
])

// insert featured products
db.products.insertMany([
  { id: 1, name: "Classic White T-Shirt", price: 29.99, image: "/images/tshirt-white.jpg", category: "T-Shirts", rating: 4.5, featured: true },
  { id: 2, name: "Denim Jacket", price: 89.99, image: "/images/denim-jacket.jpg", category: "Jackets", rating: 4.8, featured: true },
  { id: 3, name: "Summer Dress", price: 49.99, image: "/images/summer-dress.jpg", category: "Dresses", rating: 4.3, featured: true },
  { id: 4, name: "Casual Pants", price: 59.99, image: "/images/casual-pants.jpg", category: "Pants", rating: 4.6, featured: true }
])
```

### Option B — Use MongoDB Compass

Connect to mongodb://localhost:27017

Create database ecommerce

Add collections subscribers, products, categories

Use Compass UI to add documents or import JSON

Option C — Seed script (Python) — put backend/seed_db.py

Create backend/seed_db.py and run it (nice for reproducibility):

# backend/seed_db.py
```py
from pymongo import MongoClient, errors
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ecommerce")
client = MongoClient(MONGO_URI)
db = client.get_default_database()

# Ensure unique index for subscribers
try:
    db.subscribers.create_index("email", unique=True)
except errors.OperationFailure:
    pass

categories = [
    {"id":1, "name":"T-Shirts", "image":"/images/category-tshirts.jpg", "count":45},
    {"id":2, "name":"Jackets", "image":"/images/category-jackets.jpg", "count":23},
    {"id":3, "name":"Dresses", "image":"/images/category-dresses.jpg", "count":34},
    {"id":4, "name":"Pants", "image":"/images/category-pants.jpg", "count":28},
]

products = [
    {"id":1, "name":"Classic White T-Shirt", "price":29.99, "image":"/images/tshirt-white.jpg", "category":"T-Shirts", "rating":4.5, "featured":True},
    {"id":2, "name":"Denim Jacket", "price":89.99, "image":"/images/denim-jacket.jpg", "category":"Jackets", "rating":4.8, "featured":True},
    {"id":3, "name":"Summer Dress", "price":49.99, "image":"/images/summer-dress.jpg", "category":"Dresses", "rating":4.3, "featured":True},
    {"id":4, "name":"Casual Pants", "price":59.99, "image":"/images/casual-pants.jpg", "category":"Pants", "rating":4.6, "featured":True},
]

db.categories.delete_many({})
db.products.delete_many({})
db.categories.insert_many(categories)
db.products.insert_many(products)

print("Seeding complete.")


Run:

# with venv activated
python seed_db.py
```

### 5) Wire backend routes to the DB (replace mock arrays)

Replace your current get_featured_products and get_categories with DB queries. Example updates to backend/app/routes.py:
```py
from flask import Blueprint, request, jsonify
from app.utils import validate_email, send_welcome_email
from app import mongo
import datetime

main = Blueprint('main', __name__)

@main.route('/api/products/featured', methods=['GET'])
def get_featured_products():
    try:
        products = list(mongo.db.products.find({"featured": True}, {"_id": 0}))
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch products'}), 500

@main.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        categories = list(mongo.db.categories.find({}, {"_id": 0}))
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch categories'}), 500

```
Note: {"_id": 0} excludes MongoDB’s ObjectId (keeps JSON clean). If you want _id, convert ObjectId to str() before jsonify or use bson.json_util.