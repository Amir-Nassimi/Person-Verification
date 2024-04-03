import cv2
from numpy.linalg import norm
from numpy import array, pi, arctan, shape
from PIL import Image
from cv2 import getRotationMatrix2D, resize, warpAffine, INTER_AREA
from ultralytics import YOLO


class Detection:

    def __init__(self, yolo_model, face_detector_score, dist_treshold, Fixed_size):
        self.yolo_model = yolo_model
        self.face_detector_score = face_detector_score
        self.dist_treshold = dist_treshold
        self.Fixed_size = Fixed_size

    def image_resize(self, image, width=None, height=None, inter=INTER_AREA):
        dim = None
        (h, w) = shape(image)[:2]

        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return resize(image, dim, interpolation=inter)

    def fix_face(self, image, left_eye, right_eye):
        angle = (arctan((right_eye[1] - left_eye[1]) /
                 (right_eye[0] - left_eye[0])) * 180) / pi
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = getRotationMatrix2D(center, (angle), 1.0)

        if w > 0 and h > 0:
            return warpAffine(image, M, (w, h))
        else:
            return image

    def detector(self, img):
        face_list, coordinations = [], []
        faces = self.yolo_model(img)
        details = faces[0].boxes.data

        if len(details) == 0:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            None, None
        else:
            for face in range(len(details)):
                score = int(details[face][4].item() * 100)

                if score < self.face_detector_score:
                    continue
                else:
                    x, y, w, h = array(details[face][:4].cpu(), dtype=int)
                    kp = array(faces[0].keypoints.data[face][:, :2].cpu(), dtype=int)
                    resize_frame = array(img)

                    try:
                        ln, wd, _ = resize_frame.shape
                    except:
                        ln, wd = resize_frame.shape

                    x_right = round(abs(kp[0, 0] - x) *
                                    (wd / resize_frame.shape[1]))
                    y_right = round(abs(kp[0, 1] - y) *
                                    (ln / resize_frame.shape[0]))
                    x_left = round(abs(kp[1, 0] - x) *
                                   (wd / resize_frame.shape[1]))
                    y_left = round(abs(kp[1, 1] - y) *
                                   (ln / resize_frame.shape[0]))
                    dist = norm((array([x_left, y_left]) -
                                array([x_right, y_right])), ord=2)

                    if dist > self.dist_treshold:
                        if x_left == x_right:
                            x_right -= 1

                        resize_frame = self.fix_face(
                            array(resize_frame), [x_left, y_left], [x_right, y_right])

                        try:
                            a, b = shape(resize_frame)
                        except:
                            a, b, _ = shape(resize_frame)

                        if a > b:
                            resize_frame = self.image_resize(
                                image=resize_frame, height=100)
                        else:
                            resize_frame = self.image_resize(
                                image=resize_frame, width=100)

                        face_list.append(resize_frame)
                        coordinations.append([x, y, w, h])

                    else:
                        continue

        return face_list, coordinations


class Summary:
    def __init__(self,
                 model_path,           # 'yolov8n-face.pt'
                 face_detector_score,  # 58
                 dist_treshold,        # 5
                 Fixed_size,           # 300
                 ):

        self.Fixed_size = Fixed_size
        self.fd = Detection(yolo_model=YOLO(model_path),
                            face_detector_score=face_detector_score,
                            dist_treshold=dist_treshold,
                            Fixed_size=self.Fixed_size)

    def Set_fix_size(self, img, fill_color=(0, 0, 0)):
        img = cv2.resize(
            img, (round(self.Fixed_size * (img.shape[1] / img.shape[0])), self.Fixed_size))
        myimg = Image.fromarray(img)
        x, y = myimg.size
        size = max(self.Fixed_size, x, y)

        fixed_img = Image.new("RGB", (size, size), fill_color)
        fixed_img.paste(myimg, (int((size - x) / 2), int((size - y) / 2)))

        return fixed_img.resize((self.Fixed_size, self.Fixed_size))

    def face_detection(self, image):
        face_list, coordinations = self.fd.detector(image)

        if (coordinations == False) or (coordinations == []):
            # No face has been detected
            return None, None, False

        else:
            # face has been detected
            final_images = []
            for img in face_list:
                final_images.append(self.Set_fix_size(array(img), fill_color=(0, 0, 0)))
            return final_images, coordinations, True
