from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('', MachineViewSet)
router.register(r'(?P<machine_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'(?P<machine_id>\d+)/rare_issues', MachineRareIssuesViewSet, basename='rare_issues')
router.register(r'(?P<machine_id>\d+)/common_issues', MachineCommonIssuesViewSet, basename='common_issues')

urlpatterns = [
    path('', include(router.urls)),
    path('reviews/all/', AllReviewsView.as_view(), name='all_reviews'),
]
