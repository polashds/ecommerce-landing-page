from flask import Blueprint, request, jsonify
from app.models.product import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products with optional filters"""
    try:
        db = request.app.config['db']
        category = request.args.get('category')
        featured = request.args.get('featured')
        
        # Convert featured to boolean if provided
        if featured is not None:
            featured = featured.lower() == 'true'
        
        products = Product.get_all(db, category=category, featured=featured)
        return jsonify({'products': products, 'count': len(products)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    try:
        db = request.app.config['db']
        product = Product.get_by_id(db, product_id)
        
        if product:
            return jsonify({'product': product}), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        db = request.app.config['db']
        categories = Product.get_categories(db)
        return jsonify({'categories': categories}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product (admin endpoint)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'price', 'category']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        db = request.app.config['db']
        product_id = Product.create(db, data)
        
        return jsonify({
            'message': 'Product created successfully',
            'product_id': product_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500