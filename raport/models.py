from django.db import models
from custom_user.models import CustomUser


class Raport(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()