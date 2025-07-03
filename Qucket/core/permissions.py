from rest_framework import permissions
from .models import User

from rest_framework import permissions

class IsApprovedEventOwner(permissions.BasePermission):
    message = "Only approved event owners can perform this action"

    def has_permission(self, request, view):
        # Allow GET/HEAD/OPTIONS for all
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # For write operations, check if user is authenticated, approved and event owner
        return (
            request.user.is_authenticated and 
            request.user.is_approved and 
            request.user.is_event_owner
        )
    
class IsEventOwner(permissions.BasePermission):
  
    message = "You must be the event owner to perform this action"

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only allowed for the event owner
        return obj.owner == request.user
    
class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
class IsApproved(permissions.BasePermission):
  class IsApproved(permissions.BasePermission):
    message = "Your account is not yet approved"

    def has_permission(self, request, view):
        # Allow GET/HEAD/OPTIONS for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # For write operations, check if user is authenticated and approved
        return request.user.is_authenticated and (
            request.user.is_approved or 
            request.user.is_superuser
        )