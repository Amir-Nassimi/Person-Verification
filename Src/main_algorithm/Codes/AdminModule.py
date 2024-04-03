from person_verification.Src.utils import FaceDetection
from person_verification.Src.main_algorithm.Modules.mydeepface import DeepFace
from numpy import array as to_array
import json


class AdminModule:

    def __init__(self,
                 face_detection_model_path,
                 dictionary_image_key,
                 dictionary_ID_key,

                 face_detection_confidence=50,
                 face_detection_dist_threshold=5,
                 face_detection_Fixed_size=300,

                 face_verification_database_path=None,
                 face_verification_model='Facenet512',
                 face_verification_facedetector='yolov8'
                 ):

        self.face_verification_database_path = face_verification_database_path
        self.face_verification_model = face_verification_model
        self.face_verification_facedetector = face_verification_facedetector
        self.dictionary_image_key = dictionary_image_key
        self.dictionary_ID_key = dictionary_ID_key

        self.face_detection_class = FaceDetection.Summary(model_path=face_detection_model_path,
                                                          face_detector_score=face_detection_confidence,
                                                          dist_treshold=face_detection_dist_threshold,
                                                          Fixed_size=face_detection_Fixed_size)

    def Create_dataset(self, people_dictionaries):
        inappropriate_format = []
        no_face_index = []
        multiple_face_index = []
        main_dataset = []

        for idx, person in enumerate(people_dictionaries):
            for idxx, on_img in enumerate(person[self.dictionary_image_key]):
                final_images, coordinations, flag = self.face_detection_class.face_detection(on_img)

                if not flag:
                    no_face_index.append([idx, idxx])
                elif len(coordinations) > 1:
                    multiple_face_index.append([idx, idxx])
                elif flag and len(coordinations) == 1:
                    embedding_objs = DeepFace.represent(img_path=to_array(final_images[0]),
                                                        model_name=self.face_verification_model,
                                                        detector_backend=self.face_verification_facedetector)
                    if len(embedding_objs) > 1:
                        multiple_face_index.append([idx, idxx])
                    else:
                        main_dataset.append([person[self.dictionary_ID_key], embedding_objs[0]['embedding']])

        if self.face_verification_database_path is not None:
            file_name = f"representations_{self.face_verification_model}.json"
            main_dataset_json = json.dumps(main_dataset)
            with open(self.face_verification_database_path + '/' + file_name, "w") as outfile:
                outfile.write(main_dataset_json)

        return main_dataset, inappropriate_format, no_face_index, multiple_face_index