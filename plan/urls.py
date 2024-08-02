from django.urls import path, include
from .views import EventViewSet, ShiftViewSet, GeneratePlannerView, AvailabilityViewSet, restore_shifts, FreeDayViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('events', EventViewSet)
router.register('shifts', ShiftViewSet)
router.register('availability', AvailabilityViewSet)
router.register('free_day', FreeDayViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate-planner/', GeneratePlannerView.as_view(), name='generate-planner'),
    path('restore-plan/', restore_shifts, name='restore-shifts'),
]