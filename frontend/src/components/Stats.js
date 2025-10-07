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