import secrets, qrcode, io
from django.core.files import File
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import *
from .serializers import UserSerializer, EventSerializer, TicketSerializer, EventSignUpSerializer, CustomerSignUpSerializer, CustomTokenObtainPairSerializer
from .permissions import IsApprovedEventOwner, IsEventOwner, IsCustomer, IsOwnerOrReadOnly, IsApproved
import secrets
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken #@csrf_exempt  # Temporarily disable CSRF for testing
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({
                'error': 'Invalid credentials',
                'detail': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

@ensure_csrf_cookie
def test_connection(request):
    if request.method == 'GET':
        return JsonResponse({
            'status': 'success',
            'message': 'GET request successful',
            'csrf_token': get_token(request)
        })
    elif request.method == 'POST':
        return JsonResponse({
            'status': 'success',
            'message': 'POST request successful',
            'received_data': request.POST or None
        })
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@ensure_csrf_cookie
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        # Get JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.pk,
            'is_event_owner': user.is_event_owner,
            'is_approved': user.is_approved
        })
    return Response({'error': 'Invalid credentials'}, status=400)


class ApproveUserView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_approved=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(is_approved=True)

class CustomerSignUpView(generics.CreateAPIView):
    serializer_class = CustomerSignUpSerializer
   # authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    def perform_create(self, serializer):
        serializer.save()

class EventOwnerSignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    #authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
       #if not self.request.user.is_authenticated:
        #raise serializers.ValidationError("You must be logged in to create events")
       serializer.save()

class EventListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser]
    #authentication_classes = [SessionAuthentication]
    permission_classes = [IsApprovedEventOwner]
    throttle_classes = [UserRateThrottle]

        
    def get_queryset(self):
       queryset = Event.objects.filter(is_cancelled=False)
       if self.request.user.is_authenticated and self.request.user.is_event_owner:
         return queryset.filter(owner=self.request.user)
       return queryset.filter(date_time__gt=timezone.now()).order_by('date_time')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        event = serializer.validated_data.get('event')
       # if event.owner != self.request.user:
       #     raise PermissionDenied("You don't own this event")
        serializer.save(owner=self.request.user)

class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    #authentication_classes = [SessionAuthentication]
    queryset = Event.objects.all()
    permission_classes = [IsEventOwner, IsApproved]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsEventOwner()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    
    def perform_destroy(self, instance):
        instance.is_cancelled = True
        instance.save()
        # next to add ticket refund logic

class TicketListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    #authentication_classes = [SessionAuthentication]
    permission_classes = [IsCustomer, IsApproved]

    def get_queryset(self):
        """Only show user's active tickets"""
        return Tickets.objects.filter(
            user=self.request.user,
            cancelled=False
        ).select_related('event')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)  # Note many=True
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Atomic ticket purchase with validation"""
        event = serializer.validated_data['event']
        
       
        if event.tickets_remaining <= 0:
            raise serializer.ValidationError({
                'event': 'Tickets sold out during processing'
            })
        
        with transaction.atomic():
           
            event = Event.objects.select_for_update().get(pk=event.pk)
            
            
            if event.tickets_remaining <= 0:
                raise serializer.ValidationError({
                    'event': 'Tickets just sold out'
                })
                
           
            qr_code = f"TKT-{secrets.token_hex(10)}"
             # Generate QR code image
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
            qr.add_data(qr_code)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer)
            
            event.tickets_remaining -= 1

            event.save()
            serializer.save(
                user=self.request.user,
                qr_code=qr_code,
                qr_code_image=File(buffer, name=f'{qr_code}.png')
            )
class TicketDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    #authentication_classes = [SessionAuthentication]
    permission_classes = [IsOwnerOrReadOnly, IsApproved]
    queryset = Tickets.objects.all()
    lookup_field = 'pk'
    lookup_url_kwarg = 'ticket_id'
    throttle_classes = [UserRateThrottle]