import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { ticketAPI } from '../api/ticket';
import {eventAPI} from '../api/event'
import { useAuth } from '../context/AuthContext';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardMedia,
  Button,
  CircularProgress,
  Alert
} from '@mui/material';

const EventDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { token, isAuthenticated } = useAuth();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const data = await eventAPI.getEventById(id);
        setEvent(data);
      } catch (err) {
        setError(err.message || 'Failed to load event');
      } finally {
        setLoading(false);
      }
    };

    fetchEvent();
  }, [id]);

  const handlePurchase = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    
    try {
      await ticketAPI.purchaseTicket(id, token);
      navigate('/my-tickets');
    } catch (err) {
      setError(err.message || 'Failed to purchase ticket');
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!event) return <Typography>Event not found</Typography>;

  return (
    <Box sx={{ mt: 4, maxWidth: 800, mx: 'auto' }}>
      <Card>
        {event.image && (
          <CardMedia
            component="img"
            height="400"
            image={event.image}
            alt={event.title}
          />
        )}
        <CardContent>
          <Typography gutterBottom variant="h3" component="div">
            {event.title}
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
            {new Date(event.date_time).toLocaleString()}
          </Typography>
          <Typography variant="body1" paragraph>
            {event.description}
          </Typography>
          <Typography variant="h6" sx={{ mt: 2 }}>
            ${event.ticket_price} • {event.tickets_remaining} tickets remaining
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={handlePurchase}
            disabled={event.tickets_remaining <= 0}
            sx={{ mt: 3 }}
          >
            {event.tickets_remaining > 0 ? 'Purchase Ticket' : 'Sold Out'}
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
};

export default EventDetail;