from django.contrib import admin

from .models import Camera


class CameraAdmin(admin.ModelAdmin):
    pass


admin.site.register(Camera, CameraAdmin)
