import { Typography, Box, Button } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();

  return (
    <Box sx={{ textAlign: 'center', mt: 4 }}>
      <Typography variant="h3" gutterBottom>
        Welcome to Quickets
      </Typography>
      <Typography variant="h5" gutterBottom>
        {isAuthenticated
          ? `Hello, ${user.username}!`
          : 'Please login or sign up to continue'}
      </Typography>
      {!isAuthenticated && (
        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center', gap: 2 }}>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/login')}
          >
            Login
          </Button>
          <Button
            variant="outlined"
            size="large"
            onClick={() => navigate('/signup/customer')}
          >
            Sign Up
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default Home;