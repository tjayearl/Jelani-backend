# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds phone_number and policy_number fields.
    """
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    policy_number = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.username  # or self.email if you want email login
