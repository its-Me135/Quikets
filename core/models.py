from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'CU', 'Customer'
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
    def is_event_owner(self):
        return self.role == self.Role.EVENT_OWNER

    def save(self, *args, **kwargs):
        if self.role == self.Role.CUSTOMER:
            self.is_approved = True
        elif self.role == self.Role.EVENT_OWNER:
            self.is_active = True
        super().save(*args, **kwargs)
        

class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tickets_remaining = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True, verbose_name="Event Image")
    thumbnail = models.ImageField(upload_to='event_thumbnails/', blank=True, null=True, verbose_name='Thumbnail Image')

class Tickets(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    purchase_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.CharField(max_length=100, unique=True)
    is_used = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
