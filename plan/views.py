from django.shortcuts import render
from rest_framework import viewsets, status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from django.db import transaction

from datetime import datetime, timedelta, time

from .models import Event, Shift, GeneratedPlanner, FreeDay, Availability, WeekendEvent, HolyDay
from .serializers import EventSerializer, ShiftSerializer, AvailabilitySerializer, FreeDaySerializer, DataRangeSerializer, WeekendEventSerializer, HolyDaySerializer

from custom_user.models import CustomUser

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.select_related('shift', 'user').all()
    
    @action(detail=True, methods=['POST'])
    def add_overtime(self, request, pk=None):
        event = self.get_object()
        overtime = request.data.get('overtime')
        
        if overtime == None:
            return Response({"error": "Musisz podać nadgodziny"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            overtime_value = int(overtime)
            event.overtime = overtime_value
            event.save()
            return Response({'status': 'Nadgodizny Dodane'}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Invalid overtime value.'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'])
    def change_event_to_freeday(self, request, pk=None):
        event = self.get_object()
        user = event.user
        date = event.date
        
        events_to_delete = Event.objects.filter(user=user, date=date)
        events_deleted_count = events_to_delete.count()
        events_to_delete.delete()
        
        reason = request.data.get('reason', 'Brak powodu')
        free_day, created = FreeDay.objects.get_or_create(user=user, date=date, defaults={'reason': reason})
        
        if created:
            return Response({'status': 'Zmienione na dzień wolny'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Dzień wolny już istnieje'}, status=status.HTTP_400_BAD_REQUEST)
            

class ShiftViewSet(viewsets.ModelViewSet):
    serializer_class = ShiftSerializer
    queryset = Shift.objects.all()

class WeekendEventViewSet(viewsets.ModelViewSet):
    serializer_class = WeekendEventSerializer
    queryset = WeekendEvent.objects.select_related('shift', 'user').all()
    
    
class HolyDayViewSet(viewsets.ModelViewSet):
    serializer_class = HolyDaySerializer
    queryset = HolyDay.objects.all()
    
    def perform_create(self, serializer):
        holy_day_data = serializer.validated_data
        name = holy_day_data.get('name')
        date = holy_day_data.get('date')
        
        # Kiedyś jak będą grupy dodać filtr po grupie
        users = CustomUser.objects.all()
        
        holy_days = []
        
        for user in users:
            holy_day = HolyDay(user=user, name=name, date=date)
            holy_days.append(holy_day)

        HolyDay.objects.bulk_create(holy_days)
        


class FreeDayViewSet(viewsets.ModelViewSet):
    serializer_class = FreeDaySerializer
    queryset = FreeDay.objects.select_related('user').all()

    def create(self, request, *args, **kwargs):
        data_serializer = DataRangeSerializer(data=request.data)
        if data_serializer.is_valid():
            start_date = data_serializer.validated_data['start_date']
            end_date = data_serializer.validated_data['end_date']
            reason = data_serializer.validated_data['reason']
            user = request.user if request.user.is_authenticated else None
            
            if not user:
                return Response({'error': 'User musi byc zalogowany'}, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                return Response({'error': 'Start date must be before end date'}, status=status.HTTP_400_BAD_REQUEST)
            current_date = start_date
            free_days = []

            while current_date <= end_date:
                if Event.objects.filter(user=user, date=current_date).exists():
                    Event.objects.filter(user=user, date=current_date).delete()
                if WeekendEvent.objects.filter(user=user, date=current_date).exists():
                    WeekendEvent.objects.filter(user=user, date=current_date).delete()
                if FreeDay.objects.filter(user=user, date=current_date).exists():
                    FreeDay.objects.filter(user=user, date=current_date).delete()
                # if HolyDay.objects.filter(user=user, date=current_date).exists():
                #     HolyDay.objects.filter(user=user, date=current_date).delete()
                    
                free_day = FreeDay(user=user, date=current_date, reason=reason)
                free_days.append(free_day)
                current_date += timedelta(days=1)

            FreeDay.objects.bulk_create(free_days)

            return Response({'message': 'Free days created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
        today = datetime.now().date()
        year = today.year
        month = today.month + 1
        
        if month > 12:
            month = 1
            year += 1

        if GeneratedPlanner.objects.filter(year=year, month=month).exists():
            return Response({"detail": "Grafik na ten miesiąc został już wygenerowany."}, status=status.HTTP_400_BAD_REQUEST)

        num_days_in_month = days_in_month(year, month)

        shifts = Shift.objects.prefetch_related('users').all()
        generated_events = []
        generated_weekends = []

        last_day_of_prev_month = datetime(year, month, 1) - timedelta(days=1)
        events_on_last_day = Event.objects.filter(date=last_day_of_prev_month).select_related('shift')
        shift_last_events = {}
        for event in events_on_last_day:
            shift_last_events[event.shift_id] = event

        shift_hours = {}

        for shift in shifts:
            last_shift_event = shift_last_events.get(shift.id)
            if last_shift_event:
                shift_hours[shift.id] = (last_shift_event.start_time, last_shift_event.end_time)
            else:
                shift_hours[shift.id] = (shift.start_time, shift.end_time)

        try:
            with transaction.atomic():
                def generate_events_for_day(date, is_weekend, is_holyday):
                    central_users = CustomUser.objects.filter(is_central=True)
                    for user in central_users:
                        if is_holyday:
                            continue
                        elif is_weekend:
                            weekend_event = WeekendEvent(
                                user=user,
                                date=date,
                            )
                            generated_weekends.append(weekend_event)
                        else:
                            event = Event(
                                user=user,
                                date=date,
                                start_time=time(7, 30),
                                end_time=time(15, 30),
                            )
                            generated_events.append(event)

                    for shift in shifts:
                        users = shift.users.all()
                        shift_start_time, shift_end_time = shift_hours[shift.id]
                        for user in users:
                            if is_holyday:
                                continue
                            elif is_weekend:
                                weekend_event = WeekendEvent(
                                    user=user,
                                    date=date,
                                    shift=shift,
                                )
                                generated_weekends.append(weekend_event)
                            else:
                                event = Event(
                                    user=user,
                                    date=date,
                                    shift=shift,
                                    start_time=shift_start_time,
                                    end_time=shift_end_time,
                                )
                                generated_events.append(event)

                for day in range(1, num_days_in_month + 1):
                    current_date = datetime(year, month, day).date()
                    is_last_sunday = current_date.weekday() == 6 and day == num_days_in_month
                    is_last_saturday = current_date.weekday() == 5 and day == num_days_in_month
                    is_first_sunday = current_date.weekday() == 6 and day == 1

                    if current_date.weekday() == 0 or is_first_sunday:
                        for shift in shifts:
                            shift_hours[shift.id] = rotate_working_hours(*shift_hours[shift.id])
                            
                    is_holyday = HolyDay.objects.filter(date=current_date).exists()

                    if current_date.weekday() < 5:
                        generate_events_for_day(current_date, is_weekend=False, is_holyday=is_holyday)
                    else:
                        generate_events_for_day(current_date, is_weekend=True, is_holyday=is_holyday)
                    
                    if is_last_sunday or is_last_saturday:
                        for shift in shifts:
                            shift_hours[shift.id] = rotate_working_hours(*shift_hours[shift.id])

                Event.objects.bulk_create(generated_events, batch_size=1000)
                WeekendEvent.objects.bulk_create(generated_weekends, batch_size=1000)
                GeneratedPlanner.objects.create(year=year, month=month)

        except Exception as e:
            return Response({"detail": f"Błąd podczas generowania grafików: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = EventSerializer(generated_events, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def restore_plan(request):
    today = datetime.now().date()
    year = today.year
    month = today.month + 1
    if month > 12:
        month = 1
        year += 1
    try:
        with transaction.atomic():
            Event.objects.filter(date__year=year, date__month=month).delete()
            WeekendEvent.objects.filter(date__year=year, date__month=month).delete()

            GeneratedPlanner.objects.filter(year=year, month=month).delete()

    except Exception as e:
        return Response({"detail": f"Błąd podczas przywracania planu: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'Shifts restored to initial state'}, status=status.HTTP_200_OK)
    


class AvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = AvailabilitySerializer
    queryset = Availability.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user if request.user.is_authenticated else None)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def set_acceptance_to_true(self, request, *args, **kwargs):
        availability  = self.get_object()
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        
        if not start_time or not end_time: 
            return Response({'detail': 'Musisz podać godzine początkową i końcową'}, status=status.HTTP_400_BAD_REQUEST)
        
        availability.acceptance = 'accepted'
        availability.save()
        
        WeekendEvent.objects.create(
            user=availability.user,
            date=availability.date,
            start_time=start_time,
            end_time=end_time,
        )
        
        return Response({'status': 'acceptance set True Event Created'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def set_acceptance_to_false(self, request, *args, **kwargs):
        availability = self.get_object()
        
        availability.acceptance = 'rejected'
        availability.save()
        
        return Response({'status': 'acceptance set as False'}, status=status.HTTP_200_OK)