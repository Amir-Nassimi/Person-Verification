from person_verification.Src.utils import CommonPose
from person_verification.Src.utils import FaceVerification


class TrackingSystem:

    def __init__(self,
                 pose_detection_model_path,
                 face_verification_database_path,

                 pose_detection_device='cpu',  # str: 'gpu', 'cpu'
                 pose_detection_body_size=50 / 1080,  # flt: (pixles in width of body)/(pixles in width of frame)
                 pose_detection_body_ratio=1.5,  # flt: (pixles in height of body)/(pixles in width of body)
                 pose_detection_contrast=1.2,  # flt: [1 - 3]
                 pose_detection_brightness=1.2,  # flt: [1 - 3]
                 pose_detection_sharpening=3,  # int: [1 - 4]
                 pose_detection_score_conf=0.5,  # int: [40 -  90]
                 pose_detection_dist_threshold=10,  # int: [10 - 150]
                 pose_detection_fixed_size=300,  # int: [50 - 500]

                 face_verification_model='Facenet512',
                 # str: 'VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'ArcFace'
                 face_verification_metric='euclidean_l2',  # str: 'cosine', 'euclidean', 'euclidean_l2'
                 face_verification_facedetector='yolov8',
                 # str: 'opencv', 'retinaface', 'mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8'
                 face_verification_k_reg_mean_th=0.9,  # flt: [0 - 2]
                 face_verification_k_reg_sing_th=0.7,  # flt: [0 - 2]
                 face_verification_k_str_mean_th=0,  # flt: [0 - 2]
                 face_verification_k_str_sing_th=0,  # flt: [0 - 2]
                 face_verification_un_mean_th=100,  # flt: [0 - 2]
                 face_verification_un_sing_th=100,  # flt: [0 - 2]
                 face_verification_representations=[],

                 emotion_recognition_flag=False,
                 emotion_recognition_actions=['age', 'gender', 'emotion']
                 ):

        self.pose_detection_class = CommonPose.Summary(yolo_path=pose_detection_model_path,
                                                       contrast=pose_detection_contrast,
                                                       brightness=pose_detection_brightness,
                                                       sharpening=pose_detection_sharpening,
                                                       Fixed_size=pose_detection_fixed_size,
                                                       device=pose_detection_device,
                                                       conf=pose_detection_score_conf,
                                                       dist_threshold=pose_detection_dist_threshold,
                                                       body_size=pose_detection_body_size,
                                                       body_ratio=pose_detection_body_ratio)

        self.face_verification_class = FaceVerification.Summary(db_path=face_verification_database_path,
                                                                mymodel=face_verification_model,
                                                                mymetric=face_verification_metric,
                                                                myfacedetector=face_verification_facedetector,
                                                                known_regular_mean_thr=face_verification_k_reg_mean_th,
                                                                known_regular_single_thr=face_verification_k_reg_sing_th,
                                                                known_strict_mean_thr=face_verification_k_str_mean_th,
                                                                known_strict_single_thr=face_verification_k_str_sing_th,
                                                                unknown_mean_thr=face_verification_un_mean_th,
                                                                unknown_single_thr=face_verification_un_sing_th,
                                                                arg_representations=face_verification_representations,
                                                                emotion_flag=emotion_recognition_flag,
                                                                emotion_actions=emotion_recognition_actions,
                                                                device=pose_detection_device)


    def track(self, image_list):
        all_results, detected_images, image_info = self.pose_detection_class.extraction(image_list)

        if detected_images == []:
            return None, False
        else:
            result = self.face_verification_class.my_verification(all_results, detected_images, image_info)
            return result, True
