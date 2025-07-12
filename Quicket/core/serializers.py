from rest_framework import serializers
from .models import *
from django.utils import timezone
from datetime import datetime, time, date
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_event_owner', 'is_approved', 'role', 'phone', 'email_verified']
        read_only_fields = ['role']

class EventSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=User.Role.EVENT_OWNER,
            owner=True,  # Set owner to True for event owners
            is_active=True,
            is_approved=False
        )

class CustomerSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        return User.objects.create_user(
            **validated_data,
            role=User.Role.CUSTOMER,
            is_approved=True  # Auto-approve
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['owner','created_at', 'is_cancelled']

def validate_date_time(self, value):
    # Get current time (timezone-aware)
    now = timezone.now()
    
    # Handle time-only input
    if isinstance(value, time):
        # Combine with today's date and make timezone-aware
        naive_datetime = datetime.combine(now.date(), value)
        value = timezone.make_aware(naive_datetime)
    
    # Handle datetime input
    elif isinstance(value, datetime):
        # Convert naive datetime to timezone-aware if needed
        if timezone.is_naive(value):
            value = timezone.make_aware(value)
    else:
        raise serializers.ValidationError("Expected datetime or time object")

    # Now both value and now are timezone-aware
    if value <= now:
        raise serializers.ValidationError("Event must be in the future")
    
    return value
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    
class TicketSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.filter(is_cancelled=False),
        write_only=True  # Only need ID for creation
    )
    
    class Meta:
        model = Tickets
        fields = ['id', 'event', 'purchase_date', 'qr_code', 'is_used', 'cancelled']
        read_only_fields = ['user', 'purchase_date', 'qr_code', 'is_used', 'cancelled']

    def validate(self, data):
        try:
            event = data.get('event')
            
            if not event:
                raise serializers.ValidationError({
                    'event': 'Event selection is required'
                })
            
            # Business rule validations
            if event.is_cancelled:
                raise serializers.ValidationError({
                    'event': 'Cannot book tickets for cancelled events'
                })
                
           # if not event.is_approved:
            #    raise serializers.ValidationError({
             #       'event': 'Event is not yet approved'
              #  })
                
            if event.tickets_remaining <= 0:
                raise serializers.ValidationError({
                    'event': 'No tickets available'
                })
                
            return data
            
        except Exception as e:
            raise serializers.ValidationError({
                'non_field_errors': str(e)
            })
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_event_owner'] = user.is_event_owner
        token['is_approved'] = user.is_approved

        return token