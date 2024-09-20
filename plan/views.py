from django.shortcuts import render
from rest_framework import viewsets, status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, timedelta
from django.db.models.signals import pre_save, post_save
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Event, Shift, GeneratedPlanner, FreeDay, Availability, ShiftBackup, WeekendEvent
from .serializers import EventSerializer, ShiftSerializer, AvailabilitySerializer, FreeDaySerializer, DataRangeSerializer, WeekendEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class ShiftViewSet(viewsets.ModelViewSet):
    serializer_class = ShiftSerializer
    queryset = Shift.objects.all()

class WeekendEventViewSet(viewsets.ModelViewSet):
    serializer_class = WeekendEventSerializer
    queryset = WeekendEvent.objects.all()


class FreeDayViewSet(viewsets.ModelViewSet):
    serializer_class = FreeDaySerializer
    queryset = FreeDay.objects.all()

    def create(self, request, *args, **kwargs):
        data_serializer = DataRangeSerializer(data=request.data)
        if data_serializer.is_valid():
            start_date = data_serializer.validated_data['start_date']
            end_date = data_serializer.validated_data['end_date']
            reason = data_serializer.validated_data['reason']
            user = request.user if request.user.is_authenticated else None

            if start_date > end_date:
                return Response({'error': 'Start date must be before end date'}, status=status.HTTP_400_BAD_REQUEST)

            current_date = start_date
            free_days = []

            while current_date <= end_date:
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

def pre_save_receiver(sender, instance, **kwargs):
    pass

def post_save_receiver(sender, instance, **kwargs):
    pass


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from datetime import datetime, timedelta
from .models import Event, Shift, GeneratedPlanner, ShiftBackup, WeekendEvent
from .serializers import EventSerializer


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
        month = today.month + 1  # Zawsze generujemy na kolejny miesiąc
        
        if month > 12:
            month = 1
            year += 1

        # Sprawdzenie, czy grafik już istnieje dla danego miesiąca
        if GeneratedPlanner.objects.filter(year=year, month=month).exists():
            return Response({"detail": "Grafik na ten miesiąc został już wygenerowany."}, status=status.HTTP_400_BAD_REQUEST)

        num_days_in_month = days_in_month(year, month)
        current_date = datetime(year, month, 1).date()

        shifts = Shift.objects.all()
        generated_events = []
        generated_weekends = []

        # Zapisz końcowe godziny pracy dla każdej zmiany z poprzedniego miesiąca
        last_day_of_prev_month = datetime(year, month, 1) - timedelta(days=1)
        shift_hours = {}

        for shift in shifts:
            last_shift_of_prev_month = Event.objects.filter(shift=shift, date=last_day_of_prev_month).last()
            if last_shift_of_prev_month:
                shift_hours[shift.id] = (last_shift_of_prev_month.start_time, last_shift_of_prev_month.end_time)
            else:
                # Ustaw domyślne godziny startowe dla zmiany, jeśli brak grafików z poprzedniego miesiąca
                shift_hours[shift.id] = (shift.start_time, shift.end_time)

        # Logika generowania grafików
        with transaction.atomic():
            # Backup zmiany przed aktualizacją
            for shift in shifts:
                backup = ShiftBackup.objects.create(
                    start_time=shift.start_time,
                    end_time=shift.end_time,
                    name=shift.name, 
                    description=shift.description,
                )
                backup.users.set(shift.users.all())  # Poprawka w przypisaniu użytkowników

            # Rotowanie godzin i generowanie grafików
            for day in range(1, num_days_in_month + 1):
                if current_date.weekday() == 0:  # Jeśli poniedziałek, rotujemy godziny dla każdej zmiany
                    for shift in shifts:
                        shift_hours[shift.id] = rotate_working_hours(*shift_hours[shift.id])

                # Dni robocze (poniedziałek-piątek)
                if current_date.weekday() < 5:
                    for shift in shifts:
                        shift.refresh_from_db()
                        users = shift.users.all()
                        for user in users:
                            event = Event(
                                user=user,
                                date=current_date,
                                shift=shift,
                                start_time=shift_hours[shift.id][0],
                                end_time=shift_hours[shift.id][1],
                            )
                            generated_events.append(event)
                else:
                    # Weekendy
                    for shift in shifts:
                        shift.refresh_from_db()
                        users = shift.users.all()
                        for user in users:
                            weekend_event = WeekendEvent(
                                user=user,
                                date=current_date,
                                shift=shift,
                            )
                            generated_weekends.append(weekend_event)

                current_date += timedelta(days=1)

            # Zbiorcze zapisywanie eventów i grafików weekendowych
            Event.objects.bulk_create(generated_events)
            WeekendEvent.objects.bulk_create(generated_weekends)
            GeneratedPlanner.objects.create(year=year, month=month)

        # Zwróć wygenerowane grafiki
        serializer = EventSerializer(generated_events, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    


@api_view(['POST'])
def restore_shifts(request):
    today = datetime.now().date()
    year = today.year
    month = today.month + 1
    if month > 12:
        month = 1
        year += 1
    Event.objects.filter(date__year=year, date__month=month).delete()

    Shift.objects.all().delete()

    backups = ShiftBackup.objects.all()
    for backup in backups:
        shift = Shift.objects.create(
            start_time=backup.start_time,
            end_time=backup.end_time,
            name=backup.name,
            description=backup.description
        )
        shift.users.set(backup.users.all())
    
    backups.delete()
    
    GeneratedPlanner.objects.filter(year=year, month=month).delete()

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