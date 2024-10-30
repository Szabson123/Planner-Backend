from rest_framework import serializers

from .models import *
from custom_user.models import CustomUser


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'location', 'description']
        

class ReviewSerializer(serializers.ModelSerializer):
    machine_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'machine_name' ,'date', 'description', 'done']
        
    def get_machine_name(self, obj):
        return obj.machine.name
    