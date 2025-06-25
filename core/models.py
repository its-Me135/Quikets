from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CU', 'Customer'
        VENUE_OWNER = 'VO', 'Venue Owner'
        ADMIN = 'AD', 'Admin'
        EVENT_OWNER = 'EO', 'Event Owner'

    role = models.CharField(max_length=2, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=10, blank=True)
    email_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER
    
    @property
    def is_venue_owner(self):
        return self.role == self.Role.VENUE_OWNER
    
    @property
    def is_event_owner(self):
        return self.role == self.Role.EVENT_OWNER

    def save(self, *args, **kwargs):
        if self.role == self.Role.CUSTOMER:
            self.is_approved = True
        super().save(*args, **kwargs)
        
class Venue(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='venues')
    name = models.CharField(max_length=100)
    address = models.TextField()
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    photo = models.ImageField(upload_to='venues/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['owner', 'name'],
                name = 'UNIQUE_VENUE_name_per_owner'
            )
        ]

class Event(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tickets_remaining = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

class Tickets(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    purchase_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.CharField(max_length=100, unique=True)
    is_used = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
