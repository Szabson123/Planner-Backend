from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from datetime import datetime, timedelta

from .models import Event, Shift
from .serializers import EventSerializer, ShiftSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class ShiftViewSet(viewsets.ModelViewSet):
    serializer_class = ShiftSerializer
    queryset = Shift.objects.all()
    

class GeneratePlannerView(GenericAPIView):
    serializer_class = EventSerializer
    
    def post(self, request, *args, **kwargs):
        shifts = Shift.objects.all()
        generated_events = []
        today = datetime.now().date()
        next_day = today + timedelta(days=1)

        for shift in shifts:
            users = shift.users.all()
            for user in users:
                event = Event.objects.create(
                    user=user,
                    date=next_day,
                    shift=shift
                )
                generated_events.append(event)
                
        serializer = EventSerializer(generated_events, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)