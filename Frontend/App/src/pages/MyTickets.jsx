import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { ticketAPI } from '../api/ticket';
import { QRCodeCanvas } from 'qrcode.react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  Paper,
  useTheme
} from '@mui/material';
import { Close, Download } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const MyTickets = () => {
  const { token, user } = useAuth();
  const navigate = useNavigate();
  const theme = useTheme();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openQR, setOpenQR] = useState(false);
  const [currentQR, setCurrentQR] = useState('');
  const [currentTicket, setCurrentTicket] = useState(null);

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const data = await ticketAPI.getMyTickets(token);
        setTickets(Array.isArray(data) ? data : []);
      } catch (err) {
        setError(err.message || 'Failed to load tickets');
      } finally {
        setLoading(false);
      }
    };

    if (token) fetchTickets();
  }, [token]);

  const handleShowQR = (ticket) => {
    setCurrentQR(ticket.qr_code);
    setCurrentTicket(ticket);
    setOpenQR(true);
  };

  const handleDownloadQR = () => {
    const canvas = document.getElementById('qr-code-canvas');
    if (canvas) {
      const pngUrl = canvas
        .toDataURL('image/png')
        .replace('image/png', 'image/octet-stream');
      const downloadLink = document.createElement('a');
      downloadLink.href = pngUrl;
      downloadLink.download = `ticket-${currentQR}-${user.username}.png`;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    }
  };

  const handleCloseQR = () => {
    setOpenQR(false);
    setCurrentQR('');
    setCurrentTicket(null);
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
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        My Tickets
      </Typography>

      {tickets.length === 0 ? (
        <Paper elevation={0} sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h6">You don't have any tickets yet</Typography>
          <Button
            variant="contained"
            color="primary"
            sx={{ mt: 2 }}
            onClick={() => navigate('/events')}
          >
            Browse Events
          </Button>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {tickets.map((ticket) => (
            <Grid item key={ticket.id} xs={12} sm={6} md={4}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h5" component="div">
                    {ticket.title || 'Ticket Title'}
                  </Typography>
                  
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {ticket.purchase_date ? new Date(ticket.purchase_date).toLocaleDateString() : 'Date not specified'}
                  </Typography>

                  <Box sx={{ 
                    display: 'flex', 
                    justifyContent: 'center',
                    my: 2,
                    p: 2,
                    backgroundColor: theme.palette.grey[100],
                    borderRadius: 1
                  }}>
                    <QRCodeCanvas 
                      value={ticket.qr_code} 
                      size={120}
                      level="H"
                      fgColor={theme.palette.primary.main}
                    />
                  </Box>

                  <Typography variant="body2" sx={{ mt: 1, fontFamily: 'monospace' }}>
                    ID: {ticket.qr_code}
                  </Typography>

                  <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                    <Button
                      variant="outlined"
                      fullWidth
                      onClick={() => handleShowQR(ticket)}
                    >
                      View Ticket
                    </Button>
                    <Button
                      variant="contained"
                      fullWidth
                      onClick={() => navigate(`/events/${ticket.event_id}`)}
                      disabled={!ticket.title}
                    >
                      Event Details
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* QR Code Dialog */}
      <Dialog open={openQR} onClose={handleCloseQR} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">Your Ticket</Typography>
            <IconButton onClick={handleCloseQR}>
              <Close />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent sx={{ textAlign: 'center', py: 4 }}>
          {currentTicket && (
            <>
              <Typography variant="h5" gutterBottom>
                {currentTicket.title || 'Ticket Title'}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                {currentTicket.purchase_date ? new Date(currentTicket.purchase_date).toLocaleString() : ''}
              </Typography>
            </>
          )}

          <Box sx={{ my: 3 }}>
            <QRCodeCanvas
              id="qr-code-canvas"
              value={currentQR}
              size={256}
              level="H"
              includeMargin
              fgColor={theme.palette.primary.main}
            />
          </Box>

          <Button
            variant="contained"
            startIcon={<Download />}
            onClick={handleDownloadQR}
            sx={{ mt: 2 }}
          >
            Download QR Code
          </Button>
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default MyTickets;