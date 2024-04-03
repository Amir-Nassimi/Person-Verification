from rest_framework.serializers import ModelSerializer

from .models import Result, BodyCoordinate, FaceCoordination


class BodyCoordinateSerializer(ModelSerializer):
    class Meta:
        model = BodyCoordinate
        fields = ['x_1', 'y_1', 'x_2', 'y_2']


class FaceCoordinationSerializer(ModelSerializer):
    class Meta:
        model = FaceCoordination
        fields = ['x_1', 'y_1', 'x_2', 'y_2']


class ResultSerializer(ModelSerializer):
    body_coordinates = BodyCoordinateSerializer(many=True, read_only=False)
    face_coordinations = FaceCoordinationSerializer(many=True, read_only=False)

    class Meta:
        model = Result
        fields = ['body_image', 'face_id', 'face_known_flag',
                  'face_strict_flag', 'image_person', 'body_coordinates', 'face_coordinations']
