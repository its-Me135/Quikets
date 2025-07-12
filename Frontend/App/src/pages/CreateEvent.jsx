import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { eventAPI } from '../api/event';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Alert,
  FormControl,
  Input,
  InputLabel
} from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

const CreateEvent = () => {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    date_time: null,
    ticket_price: '',
    tickets_remaining: '',
    image: null
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, image: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formDataToSend = new FormData();
    formDataToSend.append('title', formData.title);
    formDataToSend.append('description', formData.description);
    formDataToSend.append('date_time', formData.date_time.toISOString());
    formDataToSend.append('ticket_price', formData.ticket_price);
    formDataToSend.append('tickets_remaining', formData.tickets_remaining);
    if (formData.image) {
      formDataToSend.append('image', formData.image);
    }

    try {
      await eventAPI.createEvent(formDataToSend, token);
      navigate('/events');
    } catch (err) {
      setError(err.message || 'Failed to create event');
    } finally {
      setLoading(false);
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Container maxWidth="sm">
        <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Typography component="h1" variant="h4">
            Create New Event
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ width: '100%', mt: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3, width: '100%' }}>
            <TextField
              margin="normal"
              required
              fullWidth
              label="Event Title"
              name="title"
              value={formData.title}
              onChange={handleChange}
            />

            <TextField
              margin="normal"
              required
              fullWidth
              multiline
              rows={4}
              label="Description"
              name="description"
              value={formData.description}
              onChange={handleChange}
            />

            <DateTimePicker
              label="Event Date & Time"
              value={formData.date_time}
              onChange={(newValue) => {
                                        if (newValue && newValue > new Date()) {
                                        setFormData({ ...formData, date_time: newValue });
                                         }
              }}

              slotProps={{
                textField: {
                  fullWidth: true,
                  margin: 'normal',
                  required: true
                }
              }}
              minDateTime={new Date()}
              sx={{ width: '100%', mt: 2 }}
            />

            <TextField
              margin="normal"
              required
              fullWidth
              label="Ticket Price"
              name="ticket_price"
              type="number"
              inputProps={{ 
                step: "0.01",
                min: "0"
              }}
              value={formData.ticket_price}
              onChange={handleChange}
            />

            <TextField
              margin="normal"
              required
              fullWidth
              label="Number of Tickets"
              name="tickets_remaining"
              type="number"
              inputProps={{ 
                min: "1"
              }}
              value={formData.tickets_remaining}
              onChange={handleChange}
            />

            <FormControl fullWidth margin="normal">
              <InputLabel htmlFor="image-upload">Event Image (Optional)</InputLabel>
              <br />
              <br />
              
              <Input
                id="image-upload"
                type="file"
                inputProps={{ accept: 'image/*' }}
                onChange={handleFileChange}
              />
            </FormControl>

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              {loading ? 'Creating...' : 'Create Event'}
            </Button>
          </Box>
        </Box>
      </Container>
    </LocalizationProvider>
  );
};

export default CreateEvent;