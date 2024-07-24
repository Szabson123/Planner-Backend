from rest_framework import serializers
from .models import Event, Shift
from custom_user.serializers import UserSerializer


class ShiftSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Shift
        fields = ['id', 'name', 'description', 'users', 'start_date', 'end_date']


class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    shift = ShiftSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'user', 'date', 'shift']
