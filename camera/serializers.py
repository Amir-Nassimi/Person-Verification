from rest_framework.serializers import ModelSerializer
from .models import Camera


class CameraSerializer(ModelSerializer):
    class Meta:
        model = Camera
        fields = "__all__"
