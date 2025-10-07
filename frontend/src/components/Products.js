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