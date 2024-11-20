from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import AllowAny
from .serializers import RaportSerializer
from .models import Raport
from custom_user.models import CustomUser
from rest_framework import status, viewsets


class RaportViewSet(viewsets.ModelViewSet):
    serializer_class = RaportSerializer
    queryset = Raport.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
    
    def get_queryset(self):
        return Raport.objects.all().order_by('-date')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        