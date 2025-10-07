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