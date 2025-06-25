from rest_framework import permissions
from .models import User

class IsVenueOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_venue_owner
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'venue'):
            return obj.venue.owner == request.user
        return False
    
class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
class IsApproved(permissions.BasePermission):
    """
    Allows access only to approved users (or customers who are auto-approved)
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_approved or 
            request.user.role == User.Role.CUSTOMER
        )