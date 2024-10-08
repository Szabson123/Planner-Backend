from rest_framework import serializers
from .models import Event, Shift, FreeDay, Availability
from custom_user.serializers import UserSerializer
from custom_user.models import CustomUser

class ShiftSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = Shift
        fields = ['id', 'name', 'description', 'users', 'start_time', 'end_time']

class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    shift_name = serializers.CharField(source='shift.name', read_only=True)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    class Meta:
        model = Event
        fields = ['id', 'user', 'date', 'shift_name', 'start_time', 'end_time']


class WeekendEventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    shift_name = serializers.CharField(source='shift.name', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'user', 'date', 'shift_name']


class FreeDaySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = FreeDay
        fields = ['id', 'user', 'date']
        

class AvailabilitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Availability
        fields = ['id', 'date', 'acceptance', 'user']
        read_only_fields = ['user']


class DataRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    reason = serializers.CharField(max_length=255)