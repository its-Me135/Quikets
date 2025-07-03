from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import *
from .serializers import UserSerializer, EventSerializer, TicketSerializer, EventSignUpSerializer, CustomerSignUpSerializer
from .permissions import IsApprovedEventOwner, IsEventOwner, IsCustomer, IsOwnerOrReadOnly, IsApproved
import secrets
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser

"""
@csrf_exempt
def browser_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return render(request, 'login.html')
"""

class ApproveUserView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_approved=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(is_approved=True)

class CustomerSignUpView(generics.CreateAPIView):
    serializer_class = CustomerSignUpSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    def perform_create(self, serializer):
        serializer.save()

class EventOwnerSignUpView(generics.CreateAPIView):
    serializer_class = EventSignUpSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
       if not self.request.user.is_authenticated:
        raise serializer.ValidationError("You must be logged in to create events")
       serializer.save(owner=self.request.user)

class EventListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsApprovedEventOwner]
    throttle_classes = [UserRateThrottle]

        
    def get_queryset(self):
       queryset = Event.objects.filter(is_cancelled=False)
       if self.request.user.is_authenticated and self.request.user.is_event_owner:
         return queryset.filter(owner=self.request.user)
       return queryset.filter(date_time__gt=timezone.now()).order_by('date_time')
        
    def perform_create(self, serializer):
        event = serializer.validated_data.get('event')
       # if event.owner != self.request.user:
       #     raise PermissionDenied("You don't own this event")
        serializer.save(owner=self.request.user)

class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication]
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
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsCustomer, IsApproved]

    def get_queryset(self):
        """Only show user's active tickets"""
        return Tickets.objects.filter(
            user=self.request.user,
            cancelled=False
        ).select_related('event')

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
            
            
            event.tickets_remaining -= 1
            event.save()
            serializer.save(
                user=self.request.user,
                qr_code=qr_code
            )
class TicketDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsOwnerOrReadOnly, IsApproved]
    queryset = Tickets.objects.all()
    lookup_field = 'pk'
    lookup_url_kwarg = 'ticket_id'
    throttle_classes = [UserRateThrottle]