import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI - using MONGO_URI instead of MONGODB_URI
MONGO_URI = os.getenv('MONGO_URI')

print(f"🔍 Using MONGO_URI: {MONGO_URI}")

try:
    # Test connection
    client = MongoClient(MONGO_URI)
    
    # Test the connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    # List databases
    databases = client.list_database_names()
    print(f"📊 Available databases: {databases}")
    
    # Check if ecommerce database exists and show collections
    if 'ecommerce' in databases:
        db = client.ecommerce
        collections = db.list_collection_names()
        print(f"📁 Collections in ecommerce database: {collections}")
    
    client.close()
    
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")