from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import MachineSerializer, ReviewSerializer


class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    queryset = Machine.objects.all()
    
    
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    
    def perform_create(self, serializer):
        machine_id = self.kwargs.get('machine_id')
        machine = Machine.objects.get(id=machine_id)
        serializer.save(machine=machine)
    
    def get_queryset(self):
        machine_id = self.kwargs.get('machine_id')
        return Review.objects.filter(machine__id=machine_id)

        
    @action(detail=True, methods=['POST'], serializer_class=None)
    def change_to_true_false(self, request, pk=None, machine_id=None):
        try:
            review = self.get_object()
            review.done = not review.done
            review.save()
            return Response({"status": "review changed"}, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({"error": "NIe istnieje"}, status=status.HTTP_400_BAD_REQUEST)
            
