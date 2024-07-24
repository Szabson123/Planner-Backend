from django.urls import path, include
from .views import EventViewSet, ShiftViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('', EventViewSet)
router.register('shift', ShiftViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('generate-planner/', GeneratePlannerView.as_view(), name='generate-planner'),
]