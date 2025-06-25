from django.urls import path
from . import views

urlpatterns = [
    # SignUp
    path('signup/customer/', views.CustomerSignUpView.as_view(), name='customer-signup'),
    path('signup/venue-owner/', views.VenueOwnerSignUpView.as_view(), name='venue-owner-signup'),
    path('signup/event-owner/', views.EventOwnerSignUpView.as_view(), name='event-owner-signup'),
    
    path('admin/approve-user/<int:pk>/', views.ApproveUserView.as_view(), name='approve-user'),

    # Venues
    path('venues/', views.VenueListCreateAPIView.as_view(), name='venue-list'),
    path('venues/<int:pk>/', views.VenueDetailAPIView.as_view(), name='venue-detail'),
    
    # Events
    path('events/', views.EventListCreateAPIView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetailAPIView.as_view(), name='event-detail'),
    
    # Tickets
    path('tickets/', views.TicketListCreateAPIView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', views.TicketDetailAPIView.as_view(), name='ticket-detail'),
]