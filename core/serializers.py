from rest_framework import serializers
from .models import *
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['role']

class EventSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            return User.objects.create_user(
                **validated_data,
                role=User.Role.EVENT_OWNER,
                is_approved=True  # Auto-approve
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
        read_only_fields = ['created_at', 'venue', 'is_cancelled']


    def validate_date_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Event must be in the future")
        return value
    
class TicketSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Tickets
        fields = '__all__'
        read_only_fields = ['user', 'purchase_date', 'qr_code', 'is_used', 'cancelled']

    def validate(self, data):
        if data['event'].tickets_remaining <= 0:
            raise serializers.ValidationError("No tickets remaining")
        
        if data['event'].is_cancelled:
            raise serializers.ValidationError("Event is cancelled")
        
        return data
