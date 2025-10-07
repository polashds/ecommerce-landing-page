from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import config

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize MongoDB
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_database()
        app.config['db'] = db
        print("✅ Connected to MongoDB successfully!")
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        raise
    
    # Register blueprints
    from app.routes.subscribers import subscribers_bp
    from app.routes.products import products_bp
    
    app.register_blueprint(subscribers_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api')
    
    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'API is running'}, 200
    
    return app