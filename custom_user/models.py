from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_central = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['email']