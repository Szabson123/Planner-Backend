from rest_framework import serializers
from .models import Event, Shift, FreeDay, Availability
from custom_user.serializers import UserSerializer
from custom_user.models import CustomUser
from datetime import datetime

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
    count_hours = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'user', 'date', 'shift_name', 'start_time', 'end_time', 'overtime', 'count_hours']
        
    def get_count_hours(self, obj):
        start_datetime = datetime.combine(datetime.min, obj.start_time)
        end_datetime = datetime.combine(datetime.min, obj.end_time)
        
        if end_datetime < start_datetime:
            duration = (start_datetime - end_datetime)/2
        else:
            duration = abs(end_datetime - start_datetime)
            
        hours = duration.total_seconds()/3600
        
        overtime_hours = obj.overtime if obj.overtime else 0
        total_hour = hours + overtime_hours
        
        return round(total_hour, 2)

class WeekendEventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    shift_name = serializers.CharField(source='shift.name', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'user', 'date', 'shift_name']


class HolyDaySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'user', 'date']


class FreeDaySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = FreeDay
        fields = ['id', 'user', 'date', 'reason']
        

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