from django.db import models
from custom_user.models import CustomUser


class Shift(models.Model):
    users = models.ManyToManyField(CustomUser, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)  # Dodaj to pole
    end_time = models.TimeField(null=True, blank=True)    # Dodaj to pole

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.shift.name}"
        

class GeneratedPlanner(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('year', 'month')