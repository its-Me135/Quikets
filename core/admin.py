from django.contrib import admin
from .models import User,Venue, Event, Tickets # Import your models

# Register models to show in admin
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Tickets)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_approved')
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
    approve_users.short_description = "Approve selected users"