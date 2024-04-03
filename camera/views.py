from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Camera
from .serializers import CameraSerializer


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class CRUDCameraViewSet(ModelViewSet):
    queryset = Camera.objects.all().order_by('id')
    serializer_class = CameraSerializer
    pagination_class = MyPagination
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        queryset = self.queryset
        user = User.objects.get(username='admin')
        query_set = queryset.filter(user=user)
        # query_set = queryset.filter(user=self.request.user)
        return query_set

    def retrieve(self, request, *args, **kwargs):
        try:
            camera = Camera.objects.all()
            camera_serializer = CameraSerializer(camera)
            return Response(data=camera_serializer.data, status=200)
        except Exception as exception:
            return Response(data=f"exception: {str(exception.__class__)}", status=500)

    def create(self, request, *args, **kwargs):
        try:
            camera_url = request.data['camera_url']
            first_of_ip = camera_url.split('@')[1]
            ip_address = first_of_ip.split('/')[0]
            user = User.objects.get(username='admin')
            Camera.objects.create(ip_address=ip_address,
                                  is_active=True,
                                  is_streaming=True,
                                  camera_url=camera_url,
                                  user=user).save()
            message = "the camera added"
            explanation = "the camera has been added successfully"
            return Response({"message": message, "explanation": explanation}, status=201)
        except Exception as exception:
            return Response(data=f"exception: {str(exception.__class__)}", status=500)

    def destroy(self, request, *args, **kwargs):
        pk = int(self.kwargs["pk"])
        try:
            camera = Camera.objects.get(pk=pk)

            camera.delete()

            message = "the camera deleted"
            explanation = "the camera has been deleted successfully"

            return Response({"message": message, "explanation": explanation}, status=204)
        except ObjectDoesNotExist:
            message = "the camera not found"
            explanation = "the camera does not exist"
            return Response(data={"message": message, "explanation": explanation}, status=404)

        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)
