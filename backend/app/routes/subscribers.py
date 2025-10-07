from flask import Blueprint, request, jsonify
from app.models.subscriber import Subscriber

subscribers_bp = Blueprint('subscribers', __name__)

@subscribers_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """Subscribe to newsletter"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Check if email is valid (basic check)
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check if already subscribed
        db = request.app.config['db']
        existing = Subscriber.find_by_email(db, email)
        
        if existing:
            if existing['is_active']:
                return jsonify({'message': 'Email already subscribed'}), 200
            else:
                # Reactivate subscription
                db.subscribers.update_one(
                    {'email': email.lower().strip()},
                    {'$set': {'is_active': True}}
                )
                return jsonify({'message': 'Subscription reactivated!'}), 200
        
        # Create new subscriber
        subscriber_id = Subscriber.create(db, email)
        
        return jsonify({
            'message': 'Successfully subscribed to newsletter!',
            'subscriber_id': subscriber_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscribers_bp.route('/subscribers', methods=['GET'])
def get_subscribers():
    """Get all subscribers (admin endpoint)"""
    try:
        db = request.app.config['db']
        subscribers = Subscriber.get_all(db)
        return jsonify({'subscribers': subscribers, 'count': len(subscribers)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subscribers_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """Unsubscribe from newsletter"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        db = request.app.config['db']
        success = Subscriber.unsubscribe(db, email)
        
        if success:
            return jsonify({'message': 'Successfully unsubscribed'}), 200
        else:
            return jsonify({'error': 'Email not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500