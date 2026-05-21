import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth endpoints
export const authAPI = {
  signup: (data) => api.post('/auth/signup', data),
  login: (data) => api.post('/auth/login', data),
};

// Accounts endpoints
export const accountsAPI = {
  list: (userId) => api.get('/accounts', { params: { user_id: userId } }),
  get: (accountId) => api.get(`/accounts/${accountId}`),
  create: (data) => api.post('/accounts', data),
};

// Posts endpoints
export const postsAPI = {
  list: (accountId, limit = 10) => api.get(`/accounts/${accountId}/posts`, { params: { limit } }),
  get: (postId) => api.get(`/posts/${postId}`),
};

// Analytics endpoints
export const analyticsAPI = {
  accountAnalytics: (accountId) => api.get(`/accounts/${accountId}/analytics`),
  postAnalysis: (postId) => api.get(`/posts/${postId}/analysis`),
};

// Health check
export const health = () => api.get('/health');

export default api;
