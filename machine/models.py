from django.db import models
from custom_user.models import CustomUser


class MachinePictures(models.Model):
    picture = models.ImageField(upload_to='machines/')


class Machine(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ForeignKey(MachinePictures, on_delete=models.DO_NOTHING, null=True, blank=True)
    

class Review(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class MachineRareIssues(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    data = models.DateField(null=True, blank=True)
    who_fixed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    what_problem = models.TextField(null=True, blank=True)
    how_fix = models.TextField(null=True, blank=True)
    image = models.ForeignKey(MachinePictures, on_delete=models.DO_NOTHING, null=True, blank=True)
    

class MachineKnowHow(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    added_data = models.DateField(auto_now_add=True, null=True, blank=True)
    how_to_do = models.TextField(null=True, blank=True)
    image = models.ForeignKey(MachinePictures, on_delete=models.DO_NOTHING, null=True, blank=True)
    

class MachineCommonIssues(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    added_data = models.DateField(auto_now_add=True, null=True, blank=True)
    who_to_call = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    what_problem = models.TextField(null=True, blank=True)
    how_fix = models.TextField(null=True, blank=True)
    image = models.ForeignKey(MachinePictures, on_delete=models.DO_NOTHING, null=True, blank=True)