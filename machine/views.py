from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import MachineSerializer, ReviewSerializer


class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    queryset = Machine.objects.all()
    
    @action(detail=True, methods=['GET'])
    def get_machine_reviews(self, request, pk=None):
        reviews = Review.objects.filter(machine__id=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    
    def perform_create(self, serializer):
        machine_id = self.kwargs.get('machine_id')
        machine = Machine.objects.get(id=machine_id)
        serializer.save(machine=machine)
        
