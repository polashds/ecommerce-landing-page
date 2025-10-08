# Complete E-commerce Landing Page - Production Grade Guide
## 📋 Project Overview

**What we're building:**
- Modern e-commerce landing page
- Product catalog with categories
- Newsletter subscription system
- Email notifications
- Full REST API backend
- Responsive design

---

## 🎯 Order of Operations

```
1. Environment Setup (Git, Node, Python)
2. Project Structure Creation
3. Database Setup (MongoDB)
4. Backend Development (Flask API)
5. Frontend Development (React)
6. Integration & Testing
7. Deployment Preparation
```

---

## Step 1: Environment Setup (30 minutes)

**Install Git:**
```bash
# Initialize Git
git init

# Create .gitignore
touch .gitignore
```

### 2.2 Setup .gitignore

Create `.gitignore` file:

# Backend
backend/venv/
backend/__pycache__/
backend/*.pyc
backend/.env
backend/instance/

# Frontend
frontend/node_modules/
frontend/build/
frontend/.env
frontend/.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log



### 1.1 Install Required Software
```bash
# Verify installation:
node --version
npm --version
```

**Install Python:**
```bash
# Verify:
python --version
pip --version
```

**Install MongoDB:**
```bash
# Option 1: Local Installation
# Visit https://www.mongodb.com/try/download/community

# Option 2: Use MongoDB Atlas (Cloud - Recommended for beginners)
# Visit https://www.mongodb.com/cloud/atlas
# Sign up for free tier
# Create a cluster (takes 5-10 minutes)
```

## Step 2: Project Structure Creation (10 minutes)

### 2.1 Create Project Directory

```bash
# Create main project folder
mkdir ecommerce-landing-page
cd ecommerce-landing-page

### 2.3 Create Folder Structure

```bash
# Create backend folder
mkdir backend
cd backend

# Create backend structure
mkdir app
mkdir app/models
mkdir app/routes
mkdir app/utils
touch app/__init__.py
touch app/models/__init__.py
touch app/routes/__init__.py
touch app/utils/__init__.py
touch requirements.txt
touch config.py
touch run.py

# Go back to root
cd ..

# Create frontend folder (we'll use create-react-app later)
# For now, just note we'll create it in Step 5
```

Your structure should look like:
```
ecommerce-landing-page/
├── .gitignore
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   └── __init__.py
│   │   ├── routes/
│   │   │   └── __init__.py
│   │   └── utils/
│   │       └── __init__.py
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
└── frontend/ (will create later)
```

---

## Step 3: Database Setup (15 minutes)

### 3.1 MongoDB Atlas Setup (Cloud Option - Recommended)

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a new cluster (free M0 tier)
4. Wait for cluster creation (5-10 minutes)
5. Click "Connect" → "Connect your application"
6. Copy the connection string (looks like: `mongodb+srv://username:<password>@cluster.mongodb.net/`)

### 3.2 Create Database Schema Planning

We'll store:
- **Subscribers Collection**: email, subscribed_at, is_active
- **Products Collection**: name, description, price, category, image_url, featured

---
Step-by-Step: Connect MongoDB
Step 1: Check MongoDB installation path
C:\Program Files\MongoDB\Server\7.0\bin
Step 2: Add MongoDB to your PATH (so VS Code can find it)
Press Windows Key → type “Environment Variables” → Open
In System Properties, click Environment Variables
Under “System variables” → select Path → click Edit
Click New and paste:
C:\Program Files\MongoDB\Server\7.0\bin
(Replace 7.0 with your installed version.)
Click OK → OK → OK
Step 3: Restart VS Code
Then open your VS Code terminal (choose Git Bash or PowerShell).
Run:
mongosh

Step 4: (Optional) Connect to a specific database
mongosh "mongodb://localhost:27017/mydatabase"
Step 5: (For Python projects in VS Code)
pip install pymongo


3) Configure environment variables
Create backend/.env (or use .env.local for dev). Example:
# MongoDB Connection Mongodb Atlas cloud
MONGO_URI=mongodb+srv://siddiquembio2012_db_user:vNiEHs3wGcGFvY3D@cluster0.fvmmctx.mongodb.net/ecommerce?retryWrites=true&w=majority
FLASK_ENV=development
SECRET_KEY=

# MongoDB Connection for local host:
FLASK_DEBUG=True
MONGO_URI=mongodb://localhost:27017/ecommerce
SECRET_KEY=dev-secret-key


Step 4: Create Your Database and Collection
Using MongoDB Compass (GUI - Recommended):

Download MongoDB Compass

Connect to mongodb://localhost:27017 (local) or your Atlas connection string

Create database named ecommerce

Create collection named subscribers

Using MongoDB Shell:

bash
# Start MongoDB
mongod

# In another terminal, connect
mongo

# Create database and collection
use ecommerce
db.createCollection("subscribers")
db.subscribers.insertOne({email: "test@test.com", subscribed_at: new Date(), active: true})


---

## Step 4: Backend Development (90 minutes)

### 4.1 Setup Python Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Your prompt should now show (venv)
```


### 4.2 Install Dependencies

Update `requirements.txt`:
```
Flask==3.0.0
Flask-CORS==4.0.0
pymongo==4.6.1
python-dotenv==1.0.0
dnspython==2.4.2
```

Install packages:
```bash
pip install -r requirements.txt
```

### 4.3 Create Configuration File

`backend/config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ecommerce')
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```


### 4.4 Create Environment Variables

`backend/.env`:
```
# MongoDB Connection
MONGO_URI=mongodb+srv://your-username:your-password@cluster.mongodb.net/ecommerce?retryWrites=true&w=majority

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this

# Email Configuration (optional for now)
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# EMAIL_USER=your-email@gmail.com
# EMAIL_PASSWORD=your-app-password
```


### 4.5 Create Database Models

`backend/app/models/subscriber.py`:
```python
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

```


`backend/app/models/product.py`:
```python
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
```


### 4.6 Create API Routes

`backend/app/routes/subscribers.py`:
```python
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
```

`backend/app/routes/products.py`:
```python
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
```

### 4.7 Initialize Flask App

`backend/app/__init__.py`:
```python
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
```

### 4.8 Create Run Script

`backend/run.py`:
```python
from app import create_app
import os

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

```

### 4.9 Test Backend

```bash
# Make sure you're in backend folder and venv is activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the server
python run.py
```

You should see:
```
✅ Connected to MongoDB successfully!
 * Running on http://0.0.0.0:5000
```

**Test the API:**
```bash
# In a new terminal, test health check:
curl http://localhost:5000/api/health

# Test creating a product:
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Classic T-Shirt","price":29.99,"category":"Men","description":"Comfortable cotton t-shirt","featured":true,"image_url":"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab","stock":50}'

# Test newsletter subscription:
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```


## Step 5: Frontend Development (120 minutes)

### 5.1 Create React App

```bash
# Go back to project root
cd ..


# Create React app bash was not worked changed to cmd
npx create-react-app frontend
cd frontend

# Install additional dependencies
npm install axios react-icons
# npm install -D tailwindcss postcss autoprefixer
# npx tailwindcss init -p


#  the manual config doesn't work, let's try installing Tailwind CSS globally:
npm install -g tailwindcss
tailwindcss init -p

# this specific version worked!!!!!
npm install -D tailwindcss@3.3.0
npx tailwindcss@3.3.0 init -p
```


### 5.2 Configure Tailwind CSS

`frontend/tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

`frontend/src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### 5.3 Create Environment File

`frontend/.env`:
```
REACT_APP_API_URL=http://localhost:5000/api
```

### 5.4 Create API Service

`frontend/src/services/api.js`:
```javascript
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const subscribeNewsletter = async (email) => {
  const response = await api.post('/subscribe', { email });
  return response.data;
};

export const getProducts = async (filters = {}) => {
  const params = new URLSearchParams(filters).toString();
  const response = await api.get(`/products?${params}`);
  return response.data;
};

export const getCategories = async () => {
  const response = await api.get('/categories');
  return response.data;
};

export default api;

```

### 5.5 Create Components

## Step 5.6: Create Individual Component Files

Now that you've seen the complete application working, let's organize it properly into separate files for your actual project:

### Create Component Files Structure

```bash
cd frontend/src
mkdir components
cd components
```

Create these files with the corresponding component code from the artifact:

`frontend/src/components/Header.js`:
```javascript
import React from 'react';
import { ShoppingBag, Search, Heart } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-2">
            <ShoppingBag className="h-8 w-8 text-blue-600" />
            <span className="text-2xl font-bold text-gray-900">StyleHub</span>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <a href="#home" className="text-gray-700 hover:text-blue-600 transition">Home</a>
            <a href="#products" className="text-gray-700 hover:text-blue-600 transition">Products</a>
            <a href="#categories" className="text-gray-700 hover:text-blue-600 transition">Categories</a>
            <a href="#newsletter" className="text-gray-700 hover:text-blue-600 transition">Newsletter</a>
          </nav>

          <div className="flex items-center space-x-4">
            <button className="p-2 hover:bg-gray-100 rounded-full transition">
              <Search className="h-5 w-5 text-gray-600" />
            </button>
            <button className="p-2 hover:bg-gray-100 rounded-full transition relative">
              <Heart className="h-5 w-5 text-gray-600" />
              <span className="absolute top-0 right-0 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">3</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

```


`frontend/src/components/Hero.js`:
```javascript
import React from 'react';

const Hero = () => {
  return (
    <section id="home" className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Discover Your Style
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-blue-100">
            Premium fashion for the modern you
          </p>
          <div className="flex justify-center space-x-4">
            <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition transform hover:scale-105">
              Shop Now
            </button>
            <button className="border-2 border-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition">
              Learn More
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
```

`frontend/src/components/Newsletter.js`:
```javascript
import React, { useState } from 'react';
import { Mail, Check, AlertCircle } from 'lucide-react';

// Mock API service (replace with actual API calls)
const api = {
  subscribeNewsletter: async (email) => {
    // Simulate API call
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ message: 'Successfully subscribed!' });
      }, 1000);
    });
  },
};

const Newsletter = () => {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState({ type: '', message: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email) {
      setStatus({ type: 'error', message: 'Please enter your email' });
      return;
    }

    if (!email.includes('@') || !email.includes('.')) {
      setStatus({ type: 'error', message: 'Please enter a valid email' });
      return;
    }

    setLoading(true);
    setStatus({ type: '', message: '' });

    try {
      const result = await api.subscribeNewsletter(email);
      setStatus({ type: 'success', message: result.message });
      setEmail('');
    } catch (error) {
      setStatus({ 
        type: 'error', 
        message: error.response?.data?.error || 'Failed to subscribe. Please try again.' 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="newsletter" className="py-16 bg-gradient-to-r from-blue-600 to-purple-600">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center text-white mb-8">
          <Mail className="h-16 w-16 mx-auto mb-4" />
          <h2 className="text-4xl font-bold mb-4">Join Our Newsletter</h2>
          <p className="text-xl text-blue-100">
            Get exclusive deals and updates delivered to your inbox
          </p>
        </div>

        <form onSubmit={handleSubmit} className="max-w-md mx-auto">
          <div className="flex flex-col sm:flex-row gap-4">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              className="flex-1 px-6 py-3 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-300"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Subscribing...' : 'Subscribe'}
            </button>
          </div>

          {status.message && (
            <div className={`mt-4 p-4 rounded-lg flex items-center ${
              status.type === 'success' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {status.type === 'success' ? (
                <Check className="h-5 w-5 mr-2" />
              ) : (
                <AlertCircle className="h-5 w-5 mr-2" />
              )}
              <span>{status.message}</span>
            </div>
          )}
        </form>
      </div>
    </section>
  );
};

export default Newsletter;

```


`frontend/src/components/Products.js`:
```javascript
import React, { useState, useEffect, useCallback } from 'react';
import ProductCard from './ProductCard';

// Mock API service (replace with actual API calls)
const api = {
  getProducts: async (filters = {}) => {
    // Sample product data
    const products = [
      {
        _id: '1',
        name: 'Classic White T-Shirt',
        description: 'Premium cotton blend for ultimate comfort',
        price: 29.99,
        category: 'Men',
        image_url: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
        featured: true,
      },
      {
        _id: '2',
        name: 'Denim Jacket',
        description: 'Vintage style denim with modern fit',
        price: 89.99,
        category: 'Men',
        image_url: 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=400',
        featured: true,
      },
      {
        _id: '3',
        name: 'Summer Dress',
        description: 'Lightweight and breezy for warm days',
        price: 59.99,
        category: 'Women',
        image_url: 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400',
        featured: true,
      },
      {
        _id: '4',
        name: 'Sneakers',
        description: 'Comfortable all-day wear',
        price: 79.99,
        category: 'Footwear',
        image_url: 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
        featured: false,
      },
      {
        _id: '5',
        name: 'Leather Bag',
        description: 'Elegant and spacious',
        price: 129.99,
        category: 'Accessories',
        image_url: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400',
        featured: true,
      },
      {
        _id: '6',
        name: 'Wool Sweater',
        description: 'Cozy knit for cold weather',
        price: 69.99,
        category: 'Women',
        image_url: 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400',
        featured: false,
      },
    ];

    return new Promise((resolve) => {
      setTimeout(() => {
        let filtered = products;
        if (filters.category) {
          filtered = filtered.filter(p => p.category === filters.category);
        }
        if (filters.featured !== undefined) {
          filtered = filtered.filter(p => p.featured === (filters.featured === 'true'));
        }
        resolve({ products: filtered, count: filtered.length });
      }, 500);
    });
  },
  getCategories: async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ categories: ['Men', 'Women', 'Footwear', 'Accessories'] });
      }, 300);
    });
  },
};

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [categories, setCategories] = useState([]);

  const loadProducts = useCallback(async () => {
    setLoading(true);
    try {
      const filters = selectedCategory === 'all' ? {} : { category: selectedCategory };
      const data = await api.getProducts(filters);
      setProducts(data.products);
    } catch (error) {
      console.error('Error loading products:', error);
    } finally {
      setLoading(false);
    }
  }, [selectedCategory]);

  const loadCategories = async () => {
    try {
      const data = await api.getCategories();
      setCategories(['All', ...data.categories]);
    } catch (error) {
      console.error('Error loading categories:', error);
    }
  };

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    loadProducts();
  }, [loadProducts]);

  return (
    <section id="products" className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Featured Products</h2>
          <p className="text-xl text-gray-600">Discover our handpicked collection</p>
        </div>

        {/* Category Filter */}
        <div className="flex justify-center mb-8 flex-wrap gap-2">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category.toLowerCase())}
              className={`px-6 py-2 rounded-full font-semibold transition ${
                selectedCategory === category.toLowerCase()
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading products...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {products.map((product) => (
              <ProductCard key={product._id} product={product} />
            ))}
          </div>
        )}

        {!loading && products.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">No products found in this category.</p>
          </div>
        )}
      </div>
    </section>
  );
};

export default Products;
```

`frontend/src/components/ProductCard.js`:
```javascript
import React from 'react';
import { Star } from 'lucide-react';

const ProductCard = ({ product }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
      <div className="relative">
        <img 
          src={product.image_url} 
          alt={product.name}
          className="w-full h-64 object-cover"
        />
        {product.featured && (
          <span className="absolute top-4 right-4 bg-yellow-400 text-yellow-900 px-3 py-1 rounded-full text-sm font-semibold flex items-center">
            <Star className="h-4 w-4 mr-1" fill="currentColor" />
            Featured
          </span>
        )}
      </div>
      <div className="p-4">
        <div className="text-sm text-gray-500 mb-1">{product.category}</div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{product.name}</h3>
        <p className="text-gray-600 text-sm mb-4">{product.description}</p>
        <div className="flex justify-between items-center">
          <span className="text-2xl font-bold text-blue-600">${product.price}</span>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;

```

`frontend/src/components/Stats.js`:
```javascript
import React from 'react';
import { TrendingUp, ShoppingBag, Star } from 'lucide-react';

const Stats = () => {
  const stats = [
    { icon: <TrendingUp />, value: '10K+', label: 'Happy Customers' },
    { icon: <ShoppingBag />, value: '500+', label: 'Products' },
    { icon: <Star />, value: '4.9', label: 'Average Rating' },
  ];

  return (
    <section className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 text-blue-600 rounded-full mb-4">
                {stat.icon}
              </div>
              <div className="text-3xl font-bold text-gray-900">{stat.value}</div>
              <div className="text-gray-600">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Stats;

```


`frontend/src/components/Footer.js`:
```javascript
import React from 'react';
import { ShoppingBag } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <ShoppingBag className="h-8 w-8 text-blue-400" />
              <span className="text-2xl font-bold">StyleHub</span>
            </div>
            <p className="text-gray-400">
              Your destination for premium fashion and lifestyle products.
            </p>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Shop</h3>
            <ul className="space-y-2 text-gray-400">
              <li><button className="hover:text-white transition cursor-pointer">Men</button></li>
              <li><button className="hover:text-white transition cursor-pointer">Women</button></li>
              <li><button className="hover:text-white transition cursor-pointer">Accessories</button></li>
              <li><button className="hover:text-white transition cursor-pointer">Sale</button></li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Company</h3>
            <ul className="space-y-2 text-gray-400">
              <li><button className="hover:text-white transition cursor-pointer">About Us</button></li>
              <li><button className="hover:text-white transition cursor-pointer">Contact</button></li>
              <li><button className="hover:text-white transition cursor-pointer">Careers</button></li>
              <li><button className="hover:text-white transition cursor-pointer">Blog</button></li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Support</h3>
            <ul className="space-y-2 text-gray-400">
              <li><button className="hover:text-white transition cursor-pointer">FAQ</button></li>
              <li><button className="hover:text-white transition cursor-pointer">Shipping</button></li>
              <li><button className="hover:text-white transition cursor-pointer">Returns</button></li>
              <li><button className="hover:text-white transition cursor-pointer">Privacy</button></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 StyleHub. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
```

### Main App.js

`frontend/src/App.js`:
```javascript
import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Stats from './components/Stats';
import Products from './components/Products';
import Newsletter from './components/Newsletter';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Hero />
      <Stats />
      <Products />
      <Newsletter />
      <Footer />
    </div>
  );
}

export default App;

```

## Step 6: Seed Database with Sample Data (15 minutes)

Create a script to populate your database with sample products:

**`backend/seed_data.py`:**
```python
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

```

```bash
# Clear existing data (optional)
db.products.delete_many({})

# Insert products
result = db.products.insert_many(products)
print(f"✅ Inserted {len(result.inserted_ids)} products")

client.close()
```

Run the seed script:
```bash
cd backend
python seed_data.py
```

Create a test script `backend/test_api.sh`:
```bash
#!/bin/bash

echo "Testing API endpoints..."

echo "\n1. Health Check:"
curl http://localhost:5000/api/health

echo "\n\n2. Get Products:"
curl http://localhost:5000/api/products

echo "\n\n3. Subscribe to Newsletter:"
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```



### 7.2 Run Full Stack

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Visit `http://localhost:3000` and test all features!

---