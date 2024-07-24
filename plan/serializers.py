from rest_framework import serializers
from .models import Event, Shift
from custom_user.serializers import UserSerializer


class ShiftSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Shift
        fields = ['id', 'name', 'description', 'users']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'user', 'date', 'shift']
