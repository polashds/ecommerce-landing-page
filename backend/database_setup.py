from pymongo import MongoClient, ASCENDING, TEXT
import os
from dotenv import load_dotenv

load_dotenv()

def setup_database_indexes():
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client.get_database()
    
    # Create indexes for better performance
    db.products.create_index([("category", ASCENDING)])
    db.products.create_index([("featured", ASCENDING)])
    db.products.create_index([("price", ASCENDING)])
    db.products.create_index([("name", TEXT), ("description", TEXT)])
    
    db.subscribers.create_index([("email", ASCENDING)], unique=True)
    db.subscribers.create_index([("subscribed_at", ASCENDING)])
    
    print("✅ Database indexes created successfully!")
    
    client.close()

if __name__ == "__main__":
    setup_database_indexes()