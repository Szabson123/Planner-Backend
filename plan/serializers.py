from rest_framework import serializers
from .models import Event, Shift
from custom_user.serializers import UserSerializer
from custom_user.models import CustomUser


class ShiftSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = Shift
        fields = ['id', 'name', 'description', 'users', 'start_time', 'end_time']

class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    shift = ShiftSerializer(read_only=True)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    class Meta:
        model = Event
        fields = ['id', 'user', 'date', 'shift', 'start_time', 'end_time']
