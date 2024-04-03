from json import load

from PIL.Image import open as pill_img
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from camera.models import Camera
from camera.serializers import CameraSerializer
from image_gallery.models import Image
from person_verification.Src.main_algorithm.TrackingModule import TrackingSystem
from .models import Result, BodyCoordinate, FaceCoordination
from .serializers import ResultSerializer
from .tasks import camera_runner


class DetectionViewSet(ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            image_person = Image.objects.get(id=request.data['image_id'])
            find_result = Result.objects.filter(image_person=image_person)
            if find_result:
                result_serializer = ResultSerializer(find_result, many=True)
                return Response(result_serializer.data, status=200)

            file = open('person_verification/Datasets/Dataset_0/representations.json', 'rb')
            representations = load(file)
            my_tracking_system = TrackingSystem(
                pose_detection_model_path='person_verification/Models/YOLOs/yolov8s-pose.pt',
                pose_detection_super_res_path='person_verification/Models/SRmodels/ESPCN_x2.pb',
                face_verification_database_path=False,
                face_verification_representations=representations)
            frame = pill_img(image_person.image_file.path)

            res, flag = my_tracking_system.track([frame])
            match flag:
                case False:
                    message = "not detected"
                    explanation = "the person not detected"
                    return Response(data={"message": message, "explanation": explanation}, status=404)
                case True:
                    for i in res:
                        if i['ID']:
                            result = Result.objects.create(body_image=File(i['Body_image']),
                                                           face_id=i['ID'],
                                                           image_person=image_person)

                            body_coordination = BodyCoordinate.objects.create(x_1=i['Body_Coordinate'][0],
                                                                              y_1=i['Body_Coordinate'][1],
                                                                              x_2=i['Body_Coordinate'][2],
                                                                              y_2=i['Body_Coordinate'][3],
                                                                              result=result)
                            body_coordination.save()

                            face_coordination = FaceCoordination.objects.create(x_1=i['Face_Coordinate'][0],
                                                                                y_1=i['Face_Coordinate'][1],
                                                                                x_2=i['Face_Coordinate'][2],
                                                                                y_2=i['Face_Coordinate'][3],
                                                                                result=result)
                            face_coordination.save()
                            find_result = Result.objects.filter(image_person=image_person)
                            result_serializer = ResultSerializer(find_result, many=True)
                            return Response(result_serializer.data, status=200)
                        else:
                            result = Result.objects.create(body_image=File(i['Body_image']),
                                                           face_id='anonymous',
                                                           image_person=image_person)
                            result.save()

                            body_coordination = BodyCoordinate.objects.create(x_1=i['Body_Coordinate'][0],
                                                                              y_1=i['Body_Coordinate'][1],
                                                                              x_2=i['Body_Coordinate'][2],
                                                                              y_2=i['Body_Coordinate'][3],
                                                                              result=result)
                            body_coordination.save()

                            face_coordination = FaceCoordination.objects.create(x_1=i['Face_Coordinate'][0],
                                                                                y_1=i['Face_Coordinate'][1],
                                                                                x_2=i['Face_Coordinate'][2],
                                                                                y_2=i['Face_Coordinate'][3],
                                                                                result=result)
                            face_coordination.save()
                            find_result = Result.objects.filter(image_person=image_person)
                            result_serializer = ResultSerializer(find_result, many=True)
                            return Response(result_serializer.data, status=200)
        except ObjectDoesNotExist:
            message = "the image person not found"
            explanation = "the image person does not exist"
            return Response(data={"message": message, "explanation": explanation}, status=404)

        except Exception as error:
            return Response(data=f"error: {str(error.__class__)}", status=500)


class StreamCameraDetectionViewSet(ModelViewSet):
    queryset = Camera.objects.all().order_by('id')
    serializer_class = CameraSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        max_workers = int(self.kwargs["max_workers"])
        camera = Camera.objects.all()
        cameras = [camera_id.id for camera_id in camera]
        camera_runner.delay(max_workers, cameras)
        message = {"title": "started", "explanation": "the cameras stream started"}
        return Response(data=message, status=200)

    def create(self, request, *args, **kwargs):
        try:
            camera = Camera.objects.get(ip_address=request.data['ip_address'])
            camera.is_streaming = False
            camera.save()
            message = "stopped"
            explanation = "the camera stream stopped"
            return Response(data={"message": message, "explanation": explanation}, status=200)
        except ObjectDoesNotExist:
            message = "the camera not found"
            explanation = "the camera does not exist"
            return Response(data={"message": message, "explanation": explanation}, status=404)

        except Exception as exception:
            return Response(data=f"error: {str(exception.__class__)}", status=500)
