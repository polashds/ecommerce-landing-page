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