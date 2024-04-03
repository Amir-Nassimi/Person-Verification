from asyncio import run
from json import dumps
from os import system
from uuid import uuid1

import cv2
import paho.mqtt.client as mqtt
from PIL import Image
from os import getenv

from person_verification.Src.admin_module.AdminModule import AdminModule
from person_verification.Src.main_algorithm.TrackingModule import TrackingSystem
from .models import Camera
from .person_details import main


def camera_capture(camera_id):
    camera = Camera.objects.get(id=camera_id)
    client = mqtt.Client()
    client.connect(getenv("MQTT_HOST"), getenv("MQTT_PORT"), 60)
    users_details = AdminModule(face_detection_model_path='person_verification/Models/YOLOs/yolov8n-face.pt',
                                face_detection_super_res_model='person_verification/Models/SRmodels/ESPCN_x3.pb',
                                dictionary_image_key='original_image',
                                dictionary_ID_key='id')
    users_data = run(main(
        f"{getenv('CAMERA_SERVICE_SCHEME')}://{getenv('CAMERA_SERVICE_HOST')}:{getenv('CAMERA_SERVICE_PORT')}/api/owner/persons-image/"))
    users = users_details.Create_dataset(users_data)[0]

    my_tracking_system = TrackingSystem(pose_detection_model_path='person_verification/Models/YOLOs/yolov8s-pose.pt',
                                        face_verification_database_path=False,
                                        face_verification_representations=users,

                                        pose_detection_device='cpu',
                                        pose_detection_body_size=50 / 1080,
                                        pose_detection_body_ratio=1,
                                        pose_detection_contrast=1.2,
                                        pose_detection_brightness=1.2,
                                        pose_detection_sharpening=3,
                                        pose_detection_score_conf=0.5,
                                        pose_detection_dist_threshold=5,
                                        pose_detection_fixed_size=300,
                                        face_verification_model='Facenet512',
                                        face_verification_metric='euclidean_l2',
                                        face_verification_facedetector='yolov8',
                                        face_verification_k_reg_mean_th=0.9,
                                        face_verification_k_reg_sing_th=0.7,
                                        face_verification_k_str_mean_th=0,
                                        face_verification_k_str_sing_th=0,
                                        face_verification_un_mean_th=100,
                                        face_verification_un_sing_th=100)
    cam = cv2.VideoCapture()

    cam.open(camera.camera_url)

    while True:
        try:
            if camera.is_streaming:
                response = system(f"ping -c 1 {camera.ip_address}")
                if response == 0:
                    ret, frame = cam.read()

                    if ret:
                        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        result, flag = my_tracking_system.track([frame])
                        if flag:

                            for i in result[0][:-1]:
                                face_id = uuid1()
                                i['Face_image'].save(f'media/image_persons/{face_id}.jpg')
                                i['Face_image'] = f'{getenv("GATEWAY_SCHEME")}://{getenv("GATEWAY_HOST")}:{getenv("GATEWAY_PORT")}/media/image_persons/{face_id}.jpg'
                                body_id = uuid1()
                                i['Body_image'].save(f'media/image_persons/{body_id}.jpg')
                                i['Body_image'] = f'{getenv("GATEWAY_SCHEME")}://{getenv("GATEWAY_HOST")}:{getenv("GATEWAY_PORT")}/media/image_persons/{body_id}.jpg'
                                client.publish('EEE/Meta_Face', dumps(i))
                    else:
                        continue
                else:
                    camera.is_active = False
                    camera.save()
        except Exception:
            pass
