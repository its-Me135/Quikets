import { createBrowserRouter } from 'react-router-dom';
import Layout from '../components/Layout';
import Home from '../pages/Home';
import Login from '../pages/Auth/Login';
import CustomerSignup from '../pages/Auth/CustomerSignup';
import EventOwnerSignup from '../pages/Auth/EventOwnerSignup';
import Events from '../pages/Events';
import MyTickets from '../pages/MyTickets';
import CreateEvent from '../pages/CreateEvent';
import ProtectedRoute from '../components/ProtectedRoute';

// Export the router configuration directly
export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'login', element: <Login /> },
      { path: 'signup/customer', element: <CustomerSignup /> },
      { path: 'signup/event-owner', element: <EventOwnerSignup /> },
      { path: 'events', element: <Events /> },
      {
        element: <ProtectedRoute />,
        children: [
          { path: 'my-tickets', element: <MyTickets /> },
          {
            element: <ProtectedRoute roles={['EO']} />,
            children: [
              { path: 'create-event', element: <CreateEvent /> },
            ],
          },
        ],
      },
    ],
  },
]);