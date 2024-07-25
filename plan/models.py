from django.db import models
from custom_user.models import CustomUser


class WorkingHours(models.Model):
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class Shift(models.Model):
    users = models.ManyToManyField(CustomUser, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    working_hours = models.ForeignKey(WorkingHours, on_delete=models.CASCADE, related_name='shifts', null=True, blank=True)



class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_user', blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='assigned_shift', null=True, blank=True)\
        

    