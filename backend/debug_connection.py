import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

def test_connection():
    MONGO_URI = os.getenv('MONGO_URI')
    
    print("🔍 Testing MongoDB Connection...")
    print(f"Connection string: {MONGO_URI.split('@')[0]}@...")  # Hide password in output
    
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Test connection
        print("🔄 Testing connection...")
        client.admin.command('ping')
        print("✅ Connection successful!")
        
        # List databases
        print("📊 Listing databases...")
        databases = client.list_database_names()
        print(f"Available databases: {databases}")
        
        client.close()
        return True
        
    except pymongo.errors.OperationFailure as e:
        print(f"❌ Authentication failed: {e}")
        print("\n💡 Possible solutions:")
        print("1. Check your username and password in MongoDB Atlas")
        print("2. Make sure your IP is whitelisted in Network Access")
        print("3. Verify the database user has correct permissions")
        return False
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print(f"❌ Connection timeout: {e}")
        print("💡 Check your internet connection and IP whitelist")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_connection()