import cv2
import torch
from PIL import ImageEnhance
from PIL.Image import fromarray, new
from cv2 import resize
from numpy import array, zeros
from numpy.linalg import norm
from ultralytics import YOLO


class ImageEnhancement:

    def __init__(self, contrast, brightness, sharpening, Fixed_size):
        self.contrast = contrast
        self.brightness = brightness
        self.sharpening = sharpening
        self.Fixed_size = Fixed_size

    def contrast_and_brightness(self, image):
        return cv2.addWeighted(image, self.contrast, zeros(image.shape, image.dtype), 0, self.brightness)

    def sharpen(self, image):
        image = fromarray(image, 'RGB')
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(self.sharpening)

    def set_fix_size(self, img, fill_color=(0, 0, 0)):
        img = resize(img, (round(self.Fixed_size * (img.shape[1] / img.shape[0])), self.Fixed_size))
        myimg = fromarray(img)
        x, y = myimg.size
        size = max(self.Fixed_size, x, y)

        fixed_img = new("RGB", (size, size), fill_color)
        fixed_img.paste(myimg, (int((size - x) / 2), int((size - y) / 2)))
        return fixed_img.resize((self.Fixed_size, self.Fixed_size))

    def all_in_one(self, image):
        image_cb = self.contrast_and_brightness(image)
        image_sh = self.sharpen(image_cb)
        return self.set_fix_size(array(image_sh))


class CommonPose:
    def __init__(self, model, contrast, brightness, sharpening, Fixed_size, device, conf,
                 dist_threshold, body_size, body_ratio):
        self.model = model
        self.body_size = body_size
        self.body_ratio = body_ratio
        self.dist_threshold = dist_threshold
        self.conf = conf

        if device == 'gpu':
            torch.cuda.set_device(0)
            self.device = 0
        elif device == 'cpu':
            self.device = 'cpu'

        self.image_imp = ImageEnhancement(contrast, brightness, sharpening, Fixed_size)

    def body_face_detection(self, image_list):
        all_results = []
        image_info = []
        detected_images = []
        Image_index = 0

        for frame_number, frame in enumerate(image_list):
            results = self.model.predict(frame, conf=self.conf, device=self.device)
            detected_flag = False

            if results[0].keypoints.conf is None:
                all_results.append([{'Face_coordination': None,
                                     'Face_image': None,
                                     'Body_coordination': None,
                                     'Body_image': None,
                                     'ID': None,
                                     'Strict_flag': False,
                                     'age': None,
                                     'gender': None,
                                     'emotion': None},
                                    detected_flag])
                continue
            else:
                all_people = []
                image_h, image_w = results[0].orig_shape
                for person_number, person in enumerate(results[0]):
                    mybox = person[0].boxes.xyxy[0]
                    myx = [int(row[0]) for row in person[0].keypoints.xy[0]]
                    myy = [int(row[1]) for row in person[0].keypoints.xy[0]]

                    if (0 in myx[0:3]) or (0 in myy[0:3]):
                        continue

                    myw = int((mybox[2] - mybox[0]) / 2.2)
                    myh = int(myw * 1.5)

                    minx = int(myx[0] - myw / 2)
                    maxx = int(myx[0] + myw / 2)
                    miny = int(mybox[1])
                    maxy = int(mybox[1] + myh)

                    face_cord = (minx, miny, maxx, maxy)
                    body_cord = (int(mybox[0]), int(mybox[1]), int(mybox[2]), int(mybox[3]))

                    if ((self.body_size * image_w) <= (int(mybox[2]) - int(mybox[0]))) and (
                            self.body_ratio <= (int(mybox[3]) - int(mybox[1])) / (
                            int(mybox[2]) - int(mybox[0]))) and norm(
                            (array([myx[2], myy[2]]) - array([myx[1], myy[1]])), ord=2) > self.dist_threshold:

                        detected_flag = True

                        all_people.append({'Face_coordination': face_cord,
                                           'Face_image': frame.crop(face_cord),
                                           'Body_coordination': body_cord,
                                           'Body_image': frame.crop(body_cord),
                                           'ID': None,
                                           'Strict_flag': False,
                                           'age': None,
                                           'gender': None,
                                           'emotion': None})

                        detected_images.append(frame.crop(face_cord))
                        image_info.append({'Frame_number': frame_number,
                                           'Person_number': person_number,
                                           'Image_index': Image_index})
                        Image_index = Image_index + 1

                    else:
                        all_people.append({'Face_coordination': face_cord,
                                           'Face_image': frame.crop(face_cord),
                                           'Body_coordination': body_cord,
                                           'Body_image': frame.crop(body_cord),
                                           'ID': None,
                                           'Strict_flag': False,
                                           'age': None,
                                           'gender': None,
                                           'emotion': None})

                all_people.append(detected_flag)
                all_results.append(all_people)
        return all_results, detected_images, image_info


class Summary:
    def __init__(self, yolo_path, contrast, brightness, sharpening, Fixed_size, device, conf,
                 dist_threshold, body_size, body_ratio):
        self.my_extractor = CommonPose(YOLO(yolo_path), contrast, brightness, sharpening, Fixed_size,
                                       device, conf, dist_threshold, body_size, body_ratio)

    def extraction(self, image_list):
        return self.my_extractor.body_face_detection(image_list)
