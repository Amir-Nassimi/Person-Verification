from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DetectionViewSet, StreamCameraDetectionViewSet

router = DefaultRouter()

router.register('image-person-detection', DetectionViewSet)
router.register(r'stream-detection/(?P<max_workers>\d+)', StreamCameraDetectionViewSet)

urlpatterns = [
    path('', include(router.urls))
]
