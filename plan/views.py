from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from datetime import datetime, timedelta
import logging

from .models import Event, Shift
from .serializers import EventSerializer, ShiftSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class ShiftViewSet(viewsets.ModelViewSet):
    serializer_class = ShiftSerializer
    queryset = Shift.objects.all()
    

# Konfiguracja loggera
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    
    logger.debug(f"Rotating shift from {current_shift} to {rotations[next_index]}")
    print(f"Rotating shift from {current_shift} to {rotations[next_index]}")
    
    return datetime.strptime(rotations[next_index][0], "%H:%M:%S").time(), datetime.strptime(rotations[next_index][1], "%H:%M:%S").time()

class GeneratePlannerView(APIView):
    serializer_class = EventSerializer
    
    def post(self, request, *args, **kwargs):
        shifts = Shift.objects.all()
        generated_events = []
        today = datetime.now().date()
        current_date = today

        # Iterowanie przez kilka miesięcy
        num_months = 2  # Zmień na odpowiednią liczbę miesięcy, które chcesz sprawdzić
        for _ in range(num_months):
            year = current_date.year
            month = current_date.month

            # Obliczanie liczby dni w miesiącu
            num_days_in_month = days_in_month(year, month)

            logger.debug(f"Liczba dni w miesiącu {month}/{year}: {num_days_in_month}")

            while current_date <= datetime(year, month, num_days_in_month).date():
                # Sprawdzenie wartości current_date i today
                logger.debug(f"Current date: {current_date}, Weekday: {current_date.weekday()}")
                logger.debug(f"Today's date: {today}")

                # Rotacja zmian na początku każdego nowego tygodnia (poniedziałek)
                if current_date.weekday() == 0 and current_date > today:
                    logger.debug(f"Rotating shifts on {current_date}")
                    for shift in shifts:
                        original_start_time, original_end_time = shift.start_time, shift.end_time
                        shift.start_time, shift.end_time = rotate_working_hours(shift.start_time, shift.end_time)
                        shift.save()  # Zapisywanie zmian w bazie danych
                        logger.debug(f"Shift rotated from {original_start_time.strftime('%H:%M:%S')}-{original_end_time.strftime('%H:%M:%S')} to {shift.start_time.strftime('%H:%M:%S')}-{shift.end_time.strftime('%H:%M:%S')}")
                        logger.debug(f"Godzina początkowa: {shift.start_time}, Godzina końcowa: {shift.end_time}")

                # Pomijanie weekendów (sobota i niedziela) dla tworzenia wydarzeń
                if current_date.weekday() < 5:
                    for shift in shifts:
                        # Aktualizowanie zmian przed stworzeniem wydarzeń
                        shift.refresh_from_db()  # Pobiera aktualne dane zmiany z bazy danych
                        users = shift.users.all()
                        for user in users:
                            event = Event.objects.create(
                                user=user,
                                date=current_date,
                                shift=shift,
                                start_time=shift.start_time,  # Dodanie start_time
                                end_time=shift.end_time       # Dodanie end_time
                            )
                            generated_events.append(event)

                current_date += timedelta(days=1)

            current_date = datetime(year, month, num_days_in_month).date() + timedelta(days=1)
        
        serializer = EventSerializer(generated_events, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


