from django.db import models
from custom_user.models import CustomUser


class Event(models.Model):
    
    SHIFT_NUMBER_CHOICE = [
        ('0', 'none'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    shift = models.CharField(max_length=1, choices=SHIFT_NUMBER_CHOICE, default='0')