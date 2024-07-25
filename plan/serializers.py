from rest_framework import serializers
from .models import Event, Shift, WorkingHours
from custom_user.serializers import UserSerializer
from custom_user.models import CustomUser


class WorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHours
        fields = ['id', 'start_time', 'end_time']
        

class ShiftSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = Shift
        fields = ['id', 'name', 'description', 'users']


class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    shift = ShiftSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'user', 'date', 'shift']
