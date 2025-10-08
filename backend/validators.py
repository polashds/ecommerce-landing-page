import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip().lower()) is not None

def validate_product_data(data):
    """Validate product data"""
    errors = []
    
    if not data.get('name') or len(data['name']) < 2:
        errors.append("Product name must be at least 2 characters")
    
    if not data.get('description') or len(data['description']) < 10:
        errors.append("Description must be at least 10 characters")
    
    try:
        price = float(data.get('price', 0))
        if price <= 0:
            errors.append("Price must be greater than 0")
    except (ValueError, TypeError):
        errors.append("Price must be a valid number")
    
    return errors

def sanitize_input(text):
    """Basic input sanitization"""
    if not text:
        return ""
    # Remove potentially dangerous characters
    return re.sub(r'[<>]', '', text).strip()