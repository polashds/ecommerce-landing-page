from bson import ObjectId

class Product:
    """Product model for e-commerce items"""
    
    @staticmethod
    def create(db, product_data):
        """Create a new product"""
        product = {
            'name': product_data['name'],
            'description': product_data.get('description', ''),
            'price': float(product_data['price']),
            'category': product_data['category'],
            'image_url': product_data.get('image_url', ''),
            'featured': product_data.get('featured', False),
            'stock': product_data.get('stock', 0)
        }
        result = db.products.insert_one(product)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all(db, category=None, featured=None):
        """Get all products with optional filters"""
        query = {}
        if category:
            query['category'] = category
        if featured is not None:
            query['featured'] = featured
            
        products = list(db.products.find(query))
        for product in products:
            product['_id'] = str(product['_id'])
        return products
    
    @staticmethod
    def get_by_id(db, product_id):
        """Get product by ID"""
        try:
            product = db.products.find_one({'_id': ObjectId(product_id)})
            if product:
                product['_id'] = str(product['_id'])
            return product
        except:
            return None
    
    @staticmethod
    def get_categories(db):
        """Get all unique categories"""
        return db.products.distinct('category')