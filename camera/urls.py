from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CRUDCameraViewSet

router = DefaultRouter()

router.register('crud-camera', CRUDCameraViewSet)

urlpatterns = [
    path('', include(router.urls))
]
