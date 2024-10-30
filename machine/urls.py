from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('', MachineViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('machines/<int:machine_id>/reviews/', ReviewViewSet.as_view({'post': 'create'}), name='machine-reviews')
]
