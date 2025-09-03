from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    # Add extra fields if needed
    phone_number = models.CharField(max_length=20, blank=True, null=True)


class Claim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=50, blank=True)
    claim_type = models.CharField(max_length=100)
    description = models.TextField()
    date_of_incident = models.DateField(null=True, blank=True)
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    document = models.FileField(upload_to='claims/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Using self.id requires the object to be saved first.
        return f"Claim {self.id} - {self.user.username}" if self.id else f"New Claim - {self.user.username}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    METHOD_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('mpesa', 'M-Pesa'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    policy = models.ForeignKey('Policy', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES, default='card')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"


class Policy(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='policies')
    policy_number = models.CharField(max_length=50, unique=True)
    policy_type = models.CharField(max_length=100, help_text="e.g., 'Auto', 'Home', 'Life'")
    start_date = models.DateField()
    end_date = models.DateField()
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Policy {self.policy_number} for {self.user.username}"