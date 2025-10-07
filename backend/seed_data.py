import os
import pymongo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_mongodb():
    try:
        # Get MongoDB URI from environment variables - using MONGO_URI instead of MONGODB_URI
        MONGO_URI = os.getenv('MONGO_URI')
        
        print(f"🔍 Debug: MONGO_URI = {MONGO_URI}")
        
        if not MONGO_URI:
            raise ValueError("❌ MONGO_URI not found in environment variables")
        
        print("🔗 Connecting to MongoDB...")
        client = pymongo.MongoClient(MONGO_URI)
        
        # Test the connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        return client
    
    except pymongo.errors.OperationFailure as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 Please check your MongoDB username and password")
        return None
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def seed_data():
    # Connect to MongoDB
    client = connect_to_mongodb()
    
    if not client:
        print("🚫 Cannot proceed without database connection")
        return
    
    try:
        # Get database
        db = client.ecommerce
        
        # Clear existing data
        print("🗑️ Clearing existing products...")
        db.products.delete_many({})
        
        # Sample products data
        products = [
            {
                "name": "Wireless Bluetooth Headphones",
                "price": 99.99,
                "category": "Electronics",
                "image": "/images/headphones.jpg",
                "description": "High-quality wireless headphones with noise cancellation",
                "stock": 50,
                "rating": 4.5
            },
            {
                "name": "Smart Fitness Watch",
                "price": 199.99,
                "category": "Electronics", 
                "image": "/images/smartwatch.jpg",
                "description": "Track your fitness and stay connected",
                "stock": 30,
                "rating": 4.3
            },
            {
                "name": "Organic Cotton T-Shirt",
                "price": 29.99,
                "category": "Clothing",
                "image": "/images/tshirt.jpg", 
                "description": "Comfortable and sustainable cotton t-shirt",
                "stock": 100,
                "rating": 4.7
            },
            {
                "name": "Laptop Backpack",
                "price": 49.99,
                "category": "Accessories",
                "image": "/images/backpack.jpg",
                "description": "Durable backpack with laptop compartment",
                "stock": 75,
                "rating": 4.6
            },
            {
                "name": "Coffee Maker",
                "price": 79.99,
                "category": "Home & Kitchen",
                "image": "/images/coffeemaker.jpg",
                "description": "Programmable coffee maker with thermal carafe",
                "stock": 25,
                "rating": 4.4
            }
        ]
        
        # Insert products
        print("📦 Inserting products...")
        result = db.products.insert_many(products)
        print(f"✅ Successfully inserted {len(result.inserted_ids)} products")
        
        # Display inserted products
        print("\n📋 Inserted Products:")
        for product in db.products.find():
            print(f"  - {product['name']} (${product['price']})")
            
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
    finally:
        client.close()
        print("🔌 Database connection closed")

if __name__ == "__main__":
    seed_data()