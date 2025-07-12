import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
});

export const eventAPI = {
  getAllEvents: async () => {
    try {
      const response = await API.get('/events/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch events' };
    }
  },

  getEventById: async (eventId) => {
    try {
      const response = await API.get(`/events/${eventId}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch event' };
    }
  },

  createEvent: async (eventData, token) => {
    try {
      const response = await API.post('/events/', eventData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to create event' };
    }
  },

  updateEvent: async (eventId, eventData, token) => {
    try {
      const response = await API.patch(`/events/${eventId}/`, eventData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to update event' };
    }
  },

  cancelEvent: async (eventId, token) => {
    try {
      const response = await API.patch(
        `/events/${eventId}/`,
        { is_cancelled: true },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to cancel event' };
    }
  },
};