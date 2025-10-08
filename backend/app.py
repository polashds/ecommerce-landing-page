from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
import re
from datetime import datetime
import logging

load_dotenv()

app = Flask(__name__)

# Configure CORS for production
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
try:
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client.get_database()
    logger.info("✅ Connected to MongoDB successfully!")
except Exception as e:
    logger.error(f"❌ MongoDB connection failed: {e}")

# Email validation function
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        db.command('ping')
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
        "version": "1.0.0"
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        category = request.args.get('category')
        featured = request.args.get('featured')
        
        query = {}
        if category and category != 'all':
            query['category'] = category
        if featured:
            query['featured'] = featured.lower() == 'true'
        
        # Check if products collection exists
        if 'products' not in db.list_collection_names():
            return jsonify({"products": [], "count": 0, "message": "No products found"})
        
        products = list(db.products.find(query))
        
        # Convert ObjectId to string for JSON serialization
        for product in products:
            product['_id'] = str(product['_id'])
        
        return jsonify({
            "products": products,
            "count": len(products)
        })
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        return jsonify({"error": "Failed to fetch products"}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        # Check if products collection exists
        if 'products' not in db.list_collection_names():
            return jsonify({"categories": []})
        
        categories = db.products.distinct('category')
        return jsonify({"categories": categories or []})
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        return jsonify({"error": "Failed to fetch categories"}), 500

@app.route('/api/subscribe', methods=['POST'])
def subscribe_newsletter():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({"error": "Email is required"}), 400
        
        email = data['email'].strip().lower()
        
        # Validate email format
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Ensure subscribers collection exists
        if 'subscribers' not in db.list_collection_names():
            db.create_collection('subscribers')
        
        # Check if email already exists
        existing_subscriber = db.subscribers.find_one({"email": email})
        if existing_subscriber:
            return jsonify({"error": "Email already subscribed"}), 409
        
        # Add to database
        db.subscribers.insert_one({
            "email": email,
            "subscribed_at": datetime.utcnow(),
            "active": True
        })
        
        return jsonify({"message": "Successfully subscribed to newsletter!"})
        
    except Exception as e:
        logger.error(f"Error in newsletter subscription: {str(e)}")
        return jsonify({"error": "Failed to subscribe"}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)