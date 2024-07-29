from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import Event, Shift, GeneratedPlanner, FreeDay
from .serializers import EventSerializer, ShiftSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class ShiftViewSet(viewsets.ModelViewSet):
    serializer_class = ShiftSerializer
    queryset = Shift.objects.all()


def days_in_month(year, month):
    if month == 12:
        return 31
    return (datetime(year, month + 1, 1) - timedelta(days=1)).day

def rotate_working_hours(start_time, end_time):
    rotations = [
        ("06:00:00", "14:00:00"),
        ("22:00:00", "06:00:00"),
        ("14:00:00", "22:00:00")
    ]
    
    current_shift = (start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S"))
    current_index = rotations.index(current_shift)
    next_index = (current_index + 1) % len(rotations)
    
    return datetime.strptime(rotations[next_index][0], "%H:%M:%S").time(), datetime.strptime(rotations[next_index][1], "%H:%M:%S").time()

class GeneratePlannerView(APIView):
    serializer_class = EventSerializer
    
    def post(self, request, *args, **kwargs):
        shifts = Shift.objects.all()
        generated_events = []
        today = datetime.now().date()
        
        year = today.year
        month = today.month + 1
        if month > 12:
            month = 1
            year += 1

        if GeneratedPlanner.objects.filter(year=year, month=month).exists():
            return Response({"detail": "Grafik na ten miesiąc został już wygenerowany."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        num_days_in_month = days_in_month(year, month)
        current_date = datetime(year, month, 1).date()

        while current_date <= datetime(year, month, num_days_in_month).date():
            if current_date.weekday() == 0:
                for shift in shifts:
                    shift.start_time, shift.end_time = rotate_working_hours(shift.start_time, shift.end_time)
                    shift.save()

            if current_date.weekday() < 5:
                for shift in shifts:
                    shift.refresh_from_db()
                    users = shift.users.all()
                    for user in users:
                        if FreeDay.objects.filter(user=user, date=current_date):
                            continue
                        
                        event = Event.objects.create(
                            user=user,
                            date=current_date,
                            shift=shift,
                            start_time=shift.start_time,
                            end_time=shift.end_time,
                        )
                        generated_events.append(event)

            current_date += timedelta(days=1)
        
        GeneratedPlanner.objects.create(year=year, month=month)
        
        serializer = EventSerializer(generated_events, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


