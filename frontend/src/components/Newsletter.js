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