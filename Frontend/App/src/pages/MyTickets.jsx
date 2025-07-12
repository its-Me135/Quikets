import { useEffect, useState } from 'react';
import { ticketAPI } from '../api/ticket';
import { useAuth } from '../context/AuthContext';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert,
  Button
} from '@mui/material';

const MyTickets = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { token } = useAuth();

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const data = await ticketAPI.getMyTickets(token);
        // Ensure data is an array before setting it
        setTickets(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err.message || 'Failed to load tickets');
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchTickets();
    } else {
      setLoading(false);
    }
  }, [token]);

  const handleCancel = async (ticketId) => {
    try {
      await ticketAPI.cancelTicket(ticketId, token);
      // Refresh tickets after cancellation
      const data = await ticketAPI.getMyTickets(token);
      setTickets(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || 'Failed to cancel ticket');
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
        My Tickets
      </Typography>
      {tickets.length === 0 ? (
        <Typography>You don't have any tickets yet.</Typography>
      ) : (
        <Grid container spacing={3}>
          {tickets.map((ticket) => (
            <Grid item xs={12} sm={6} key={ticket.id}>
              <Card>
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    {ticket.event?.title || 'Event'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {ticket.event?.date_time 
                      ? new Date(ticket.event.date_time).toLocaleString() 
                      : 'Date not available'}
                  </Typography>
                  <Typography variant="body1" sx={{ mt: 1 }}>
                    Ticket ID: {ticket.qr_code}
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 2 }}>
                    Status: {ticket.cancelled ? 'Cancelled' : 'Active'}
                  </Typography>
                  {!ticket.cancelled && (
                    <Button
                      variant="outlined"
                      color="error"
                      onClick={() => handleCancel(ticket.id)}
                    >
                      Cancel Ticket
                    </Button>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default MyTickets;