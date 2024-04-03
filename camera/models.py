from django.db import models
from django.contrib.auth.models import User


class Camera(models.Model):
    camera_url = models.URLField(null=True)
    ip_address = models.GenericIPAddressField()
    is_active = models.BooleanField()
    is_streaming = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
