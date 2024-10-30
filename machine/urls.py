from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('', MachineViewSet)
router.register(r'(?P<machine_id>\d+)/reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
