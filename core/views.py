from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import *
from .serializers import UserSerializer,VenueSerializer, EventSerializer, TicketSerializer, EventSignUpSerializer, VenueSignUpSerializer, CustomerSignUpSerializer
from .permissions import  IsVenueOwner, IsCustomer, IsOwnerOrReadOnly, IsApproved
import secrets
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from django.db import transaction

class ApproveUserView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_approved=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(is_approved=True)

class CustomerSignUpView(generics.CreateAPIView):
    serializer_class = CustomerSignUpSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(role='CU')

class VenueOwnerSignUpView(generics.CreateAPIView):
    serializer_class = VenueSignUpSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(role='VO')

class EventOwnerSignUpView(generics.CreateAPIView):
    serializer_class = EventSignUpSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(role = 'EO')

class VenueListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = VenueSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Venue.objects.filter(owner=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class VenueDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VenueSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Venue.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class EventListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApproved]

    def get_queryset(self):
        queryset = Event.objects.filter(is_cancelled=False)
        if self.request.user.is_authenticated and self.request.user.is__venue_owner:
            return queryset.filter(venue__owner=self.request.user)
        return queryset.filter(date_time__gt=timezone.now())
    
    def perform_create(self, serializer):
        venue = serializer.validated_data.get('venue')
        if venue.owner != self.request.user:
            raise PermissionDenied("You don't own this venue")
        serializer.save()

class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsVenueOwner()]
        return [permissions.IsAuthenticatedOrReadOnly()]

class TicketListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsCustomer, IsApproved]

    def get_queryset(self):
        return Tickets.objects.filter(user=self.request.user, cancelled=False)

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        qr_code = f"TKT-{secrets.token_hex(10)}"
        
        with transaction.atomic():
            event.tickets_remaining -= 1
            event.save()
            serializer.save(user=self.request.user, qr_code=qr_code)

class TicketDetailAPIView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOrReadOnly, IsApproved]
    queryset = Tickets.objects.all()