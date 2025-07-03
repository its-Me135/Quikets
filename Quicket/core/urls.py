from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # SignUp
    path('signup/customer/', views.CustomerSignUpView.as_view(), name='customer-signup'),
    path('signup/event-owner/', views.EventOwnerSignUpView.as_view(), name='event-owner-signup'),
    
    path('admin/approve-user/<int:pk>/', views.ApproveUserView.as_view(), name='approve-user'),


    #logIn
    path('login', ObtainAuthToken.as_view(), name='login'),

    # Events
    path('events/', views.EventListCreateAPIView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetailAPIView.as_view(), name='event-detail'),
    
    # Tickets
    path('tickets/', views.TicketListCreateAPIView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', views.TicketDetailAPIView.as_view(), name='ticket-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)