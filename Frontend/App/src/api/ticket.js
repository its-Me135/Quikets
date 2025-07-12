import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
});

export const ticketAPI = {
  getMyTickets: async (token) => {
    try {
      const response = await API.get('/tickets/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch tickets' };
    }
  },

  getTicketById: async (ticketId, token) => {
    try {
      const response = await API.get(`/tickets/${ticketId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch ticket' };
    }
  },

  purchaseTicket: async (eventId, token) => {
    try {
      const response = await API.post(
        '/tickets/',
        { event: eventId },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to purchase ticket' };
    }
  },

  cancelTicket: async (ticketId, token) => {
    try {
      const response = await API.patch(
        `/tickets/${ticketId}/`,
        { cancelled: true },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to cancel ticket' };
    }
  },

  validateTicket: async (ticketId, token) => {
    try {
      const response = await API.patch(
        `/tickets/${ticketId}/`,
        { is_used: true },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to validate ticket' };
    }
  },
};