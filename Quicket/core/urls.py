from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import get_csrf, test_connection, login
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import CustomTokenObtainPairView, get_current_user


urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     path('api/user/', get_current_user, name='current-user'),
    # SignUp
    path('signup/customer/', views.CustomerSignUpView.as_view(), name='customer-signup'),
    path('signup/event-owner/', views.EventOwnerSignUpView.as_view(), name='event-owner-signup'),
    
    path('admin/approve-user/<int:pk>/', views.ApproveUserView.as_view(), name='approve-user'),

    # urls.py
    path('csrf/', get_csrf, name='get_csrf'),
    path('test-connection/', test_connection, name='test-connection'),

    #logIn
    path('login/', login, name='login'),

    # Events
    path('events/', views.EventListCreateAPIView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetailAPIView.as_view(), name='event-detail'),
    
    # Tickets
    path('tickets/', views.TicketListCreateAPIView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', views.TicketDetailAPIView.as_view(), name='ticket-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)