from django.db import models

from image_gallery.models import Image


class Result(models.Model):
    body_image = models.ImageField(upload_to="body_images/")
    face_id = models.CharField(blank=True, null=True, unique=True)
    face_known_flag = models.BooleanField(blank=True, null=True)
    face_strict_flag = models.BooleanField(blank=True, null=True)
    image_person = models.ForeignKey(Image, on_delete=models.CASCADE)


class BodyCoordinate(models.Model):
    x_1 = models.IntegerField()
    y_1 = models.IntegerField()
    x_2 = models.IntegerField()
    y_2 = models.IntegerField()
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="body_coordinates")


class FaceCoordination(models.Model):
    x_1 = models.IntegerField()
    y_1 = models.IntegerField()
    x_2 = models.IntegerField()
    y_2 = models.IntegerField()
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="face_coordinations")
