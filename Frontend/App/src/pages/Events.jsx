import { useEffect, useState } from 'react';
import { eventAPI } from '../api/event';
import { ticketAPI } from '../api/ticket';
import { useAuth } from '../context/AuthContext';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  CardMedia, 
  Button, 
  Grid,
  CircularProgress,
  Alert
} from '@mui/material';

const Events = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { token, isAuthenticated } = useAuth();

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const data = await eventAPI.getAllEvents();
        // Ensure data is an array before setting it
        setEvents(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err.message || 'Failed to load events');
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  const handlePurchase = async (eventId) => {
    if (!isAuthenticated) {
      setError('Please login to purchase tickets');
      return;
    }
    try {
      await ticketAPI.purchaseTicket(eventId, token);
      setError(null);
      // Optionally refresh events after purchase
      const data = await eventAPI.getAllEvents();
      setEvents(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || 'Failed to purchase ticket');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box mt={4}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Upcoming Events
      </Typography>
      {events.length === 0 ? (
        <Typography>No events available</Typography>
      ) : (
        <Grid container spacing={3}>
          {events.map((event) => (
            <Grid item xs={12} sm={6} md={4} key={event.id}>
              <Card>
                {event.image && (
                  <CardMedia
                    component="img"
                    height="140"
                    image={event.image}
                    alt={event.title}
                  />
                )}
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    {event.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {new Date(event.date_time).toLocaleString()}
                  </Typography>
                  <Typography variant="body1" sx={{ mt: 1 }}>
                    ${event.ticket_price} • {event.tickets_remaining} tickets left
                  </Typography>
                  <Button
                    size="small"
                    onClick={() => handlePurchase(event.id)}
                    disabled={event.tickets_remaining <= 0}
                    sx={{ mt: 2 }}
                  >
                    {event.tickets_remaining > 0 ? 'Buy Ticket' : 'Sold Out'}
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default Events;