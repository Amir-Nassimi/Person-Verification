from django.contrib import admin

from .models import Result, FaceCoordination, BodyCoordinate


class ResultAdmin(admin.ModelAdmin):
    pass


class BodyCoordinateAdmin(admin.ModelAdmin):
    pass


class FaceCoordinationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Result, ResultAdmin)
admin.site.register(BodyCoordinate, BodyCoordinateAdmin)
admin.site.register(FaceCoordination, FaceCoordinationAdmin)