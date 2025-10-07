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