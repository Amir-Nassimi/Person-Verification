from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=150)
    image_file = models.ImageField(upload_to='images/')
    description = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
