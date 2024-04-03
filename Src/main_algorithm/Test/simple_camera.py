from uuid import uuid1

import cv2
from PIL import Image
from person_verification.Src.admin_module.AdminModule import AdminModule
from person_verification.Src.main_algorithm.TrackingModule import TrackingSystem

users_details = AdminModule(face_detection_model_path='person_verification/Models/YOLOs/yolov8n-face.pt',
                            face_detection_super_res_model='person_verification/Models/SRmodels/ESPCN_x3.pb',
                            dictionary_image_key='original_image',
                            dictionary_ID_key='id')
users_data = [{}]

my_tracking_system = TrackingSystem(pose_detection_model_path='person_verification/Models/YOLOs/yolov8s-pose.pt',
                                    pose_detection_super_res_path='person_verification/Models/SRmodels/ESPCN_x2.pb',
                                    face_verification_database_path=False,
                                    face_verification_representations=users_details.create_dataset(users_data)[0])
cam = cv2.VideoCapture()

cam.open('rtsp://rtsp:Ashkan123@172.16.60.122/Streaming/channels/102')

while True:
    try:
        ret, frame = cam.read()

        if ret:
            frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            result, flag = my_tracking_system.track([frame])
            if flag:

                for i in result:
                    if isinstance(i, dict):
                        face_image = Image.open(i['Face_image'])
                        face_id = uuid1()
                        face_image.save(f'media/image_persons/{face_id}.jpg')
                        i['Face_image'] = f'media/image_persons/{face_id}.jpg'

                        print(i)

                        body_image = Image.open(i['Body_image'])
                        body_id = uuid1()
                        body_image.save(f'media/image_persons/{body_id}.jpg')
                        i['Body_image'] = f'media/image_persons/{body_id}.jpg'

        else:
            break
    except Exception:
        pass
