from datetime import datetime
from bson import ObjectId

class Subscriber:
    """Subscriber model for newsletter"""
    
    @staticmethod
    def create(db, email):
        """Create a new subscriber"""
        subscriber = {
            'email': email.lower().strip(),
            'subscribed_at': datetime.utcnow(),
            'is_active': True
        }
        result = db.subscribers.insert_one(subscriber)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_email(db, email):
        """Find subscriber by email"""
        return db.subscribers.find_one({'email': email.lower().strip()})
    
    @staticmethod
    def get_all(db):
        """Get all active subscribers"""
        subscribers = list(db.subscribers.find({'is_active': True}))
        for sub in subscribers:
            sub['_id'] = str(sub['_id'])
        return subscribers
    
    @staticmethod
    def unsubscribe(db, email):
        """Deactivate subscriber"""
        result = db.subscribers.update_one(
            {'email': email.lower().strip()},
            {'$set': {'is_active': False}}
        )
        return result.modified_count > 0