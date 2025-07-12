import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
});

// CSRF Token handling
const getCSRFToken = async () => {
  try {
    await API.get('/csrf/');
  } catch (error) {
    console.error('Error getting CSRF token:', error);
  }
};

// Initialize CSRF token
getCSRFToken();

export const authAPI = {
  login: async (credentials) => {
    try {
      const response = await API.post('/login/', credentials);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Login failed' };
    }
  },

  customerSignup: async (userData) => {
    try {
      const response = await API.post('/signup/customer/', userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Signup failed' };
    }
  },

  eventOwnerSignup: async (userData) => {
    try {
      const response = await API.post('/signup/event-owner/', userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Signup failed' };
    }
  },

  getCurrentUser: async (token) => {
    try {
      const response = await API.get('/api/user/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch user' };
    }
  },

  logout: async (token) => {
    try {
      const response = await API.post(
        '/logout/',
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Logout failed' };
    }
  },
};