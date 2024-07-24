from django.urls import path, include
from .views import EventViewSet, ShiftViewSet, GeneratePlannerView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('events', EventViewSet)
router.register('shifts', ShiftViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate-planner/', GeneratePlannerView.as_view(), name='generate-planner'),
]