import { Outlet, Link, useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Button, Typography, Box, Container } from '@mui/material';
import { useAuth } from '../context/AuthContext';

const Layout = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              Quickets
            </Link>
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            {!isAuthenticated ? (
              <>
                <Button color="inherit" onClick={() => navigate('/login')}>
                  Login
                </Button>
                <Button color="inherit" onClick={() => navigate('/signup/customer')}>
                  Sign Up
                </Button>
              </>
            ) : (
              <>
                <Button color="inherit" onClick={() => navigate('/events')}>
                  Events
                </Button>
                {user?.is_event_owner && (
                  <Button color="inherit" onClick={() => navigate('/create-event')}>
                    Create Event
                  </Button>
                )}
                <Button color="inherit" onClick={() => navigate('/my-tickets')}>
                  My Tickets
                </Button>
                <Button color="inherit" onClick={logout}>
                  Logout
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </AppBar>
      <Container sx={{ py: 4 }}>
        <Outlet />
      </Container>
    </>
  );
};

export default Layout;