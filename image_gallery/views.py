from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Image
from .serializers import ImageSerializer


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class CRUDImageViewSet(ModelViewSet):
    queryset = Image.objects.all().order_by('publish_date')
    serializer_class = ImageSerializer
    pagination_class = MyPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        queryset = self.queryset
        # query_set = queryset.filter(user=self.request.user)
        user = User.objects.get(username='admin')
        query_set = queryset.filter(user=user)
        return query_set

    def retrieve(self, request, *args, **kwargs):
        try:
            image = Image.objects.all()
            video_serializer = ImageSerializer(image, many=True)
            return Response(data=video_serializer.data, status=200)
        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)

    def create(self, request, *args, **kwargs):
        try:
            # user = User.objects.get(username=request.user.username)
            user = User.objects.get(id=1)
            Image.objects.create(title=request.data['title'],
                                 description=request.data['description'],
                                 image_file=request.data['image_file'],
                                 user=user).save()
            message = "the image created"
            explanation = "the image has been created successfully"

            return Response({"message": message, "explanation": explanation}, status=201)

        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)

    def update(self, request, *args, **kwargs):
        pk = int(self.kwargs["pk"])
        try:
            image = Image.objects.get(pk=pk)
            image.title = request.data['title']
            image.description = request.data['description']
            image.image_file = request.data['image_file']

            image.save()

            message = "the image updated"
            explanation = "the image has been updated successfully"

            return Response({"message": message, "explanation": explanation}, status=204)

        except ObjectDoesNotExist:
            message = "the image not found"
            explanation = "the image does not exist"
            return Response(data={"message": message, "explanation": explanation}, status=404)

        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)

    def destroy(self, request, *args, **kwargs):
        pk = int(self.kwargs["pk"])
        try:
            image = Image.objects.get(pk=pk)
            image.delete()
            message = "the image deleted"
            explanation = "the image has been deleted successfully"

            return Response({"message": message, "explanation": explanation}, status=204)

        except ObjectDoesNotExist:
            message = "the image not found"
            explanation = "the image does not exist"
            return Response(data={"message": message, "explanation": explanation}, status=404)

        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)
