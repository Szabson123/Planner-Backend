from django.shortcuts import render
from rest_framework import viewsets

from .models import Event, Shift
from .serializers import EventSerializer, ShiftSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class ShiftViewSet(viewsets.ModelViewSet):
    serializer_class = ShiftSerializer
    queryset = Shift.objects.all()
    