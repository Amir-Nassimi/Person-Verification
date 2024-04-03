from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CRUDImageViewSet

router = DefaultRouter()

router.register('crud-image', CRUDImageViewSet)

urlpatterns = [
    path('', include(router.urls))
]
