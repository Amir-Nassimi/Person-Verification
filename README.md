# Tracking System with CCTV

![Project Image](Documentations/Header.png)


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Output Example](#output-example)
- [License](#license)


## Introduction

The Tracking System with CCTV is a comprehensive solution designed to enhance security and personnel tracking within a specific location. This system utilizes advanced computer vision techniques to detect and verify employees based on their body features and facial characteristics.


## Features

The system consists of four primary modules:

1. **Body Detection:** This module employs computer vision algorithms to identify individuals within CCTV camera frames accurately.

2. **Body Verification:** It verifies a person's identity by comparing feature vectors extracted from the detected bodies with a labeled dataset, ensuring precise recognition.

3. **Face Detection:** This module focuses on identifying facial features within the system, providing input to the Face Verification Module.

4. **Face Verification:** It verifies individuals based on a dedicated face recognition dataset, ensuring accuracy in identity verification.

Additionally, the system incorporates decision-making capabilities and reporting functionality, where the results of both body and face verification are used to make identity decisions and generate reports, including the assignment of unique IDs to employee images.

![Project Image](Documentations/Model.jpeg)


## Installation

To install the Employee Tracking System, follow these steps:

1. Create an environment with python=3.9
   
2. If you want to run on the GPU, install `cuda 11.2`, `cudnn 8.1`,and the following libraries:

   ```bash
   pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu117
   ```

3. Install requirements in "person_verification/Src/main_algorithm":
 
   ```bash
   pip install -r requirements.txt
   ```



## Usage

To use the Tracking System, you can follow this instruction:

1. Import TrackingModule.py:

   ```python
   from person_verification.Src.main_algorithm.Codes.TrackingModule import TrackingSystem
   ```

2. If you want to use the prepared dataset, read the Json file:
   ```python
   import json

   with open('person_verification/Datasets/Representation/representations.json', "rb") as f:
        representations = json.load(f)
   ```
   
    JSON description:

    [  [`ID1`, [`512 numbers = feature vector related to the ID1 image`] ] , ... ]


* **List 1:** A list of lists (len = the number of images stored in the database)
* **List 2:** Each list in `list 1` consists of two components: a string of the person's ID, a list of 512 numbers
   
  3. Initialize the class.

     ```python
     MyTrackingSystem = TrackingSystem(pose_detection_model_path         = 'person_verification/Models/YOLOs/yolov8s-pose.pt',
                                       face_verification_database_path   = False,
                                       face_verification_representations = representations,
   
                                       pose_detection_device             = 'cpu', 
                                       pose_detection_body_size          = 50 / 1080, 
                                       pose_detection_body_ratio         = 1.5,  
                                       pose_detection_contrast           = 1.2,
                                       pose_detection_brightness         = 1.2,  
                                       pose_detection_sharpening         = 3,  
                                       pose_detection_score_conf         = 0.5, 
                                       pose_detection_dist_threshold     = 10,  
                                       pose_detection_fixed_size         = 300, 
                     
                                       face_verification_model           = 'Facenet512',
                                       face_verification_metric          = 'euclidean_l2',  
                                       face_verification_facedetector    = 'yolov8',
                                       face_verification_k_reg_mean_th   = 0.9, 
                                       face_verification_k_reg_sing_th   = 0.7, 
                                       face_verification_k_str_mean_th   = 0, 
                                       face_verification_k_str_sing_th   = 0,
                                       face_verification_un_mean_th      = 100, 
                                       face_verification_un_sing_th      = 100,
                     
                                       emotion_recognition_flag          = False,
                                       emotion_recognition_actions       = ['emotion'])
     ```

4. Upload an image:

   ```python
   from PIL import Image

   frame = Image.open('path/to/your/image')
   result, flag = MyTrackingSystem.track([frame])
   ```
   
Here is a sample for the admin module:

```python
from person_verification.Src.main_algorithm.Codes.AdminModule import AdminModule

my_admin_class = AdminModule(face_detection_model_path='person_verification/Models/YOLOs/yolov8n-face.pt',
                             dictionary_image_key='image',
                             dictionary_ID_key='username')

main_dataset, inappropriate_format, no_face_index, multiple_face_index = my_admin_class.Create_dataset(your_database)
```

## Output Example
The output of the Tracking System:

```python
[[{'Face_coordination': (875, 394, 1042, 644),
   'Face_image': <PIL.Image.Image image mode=RGB size=167x250>,
   'Body_coordination': (886, 394, 1254, 1068),
   'Body_image': <PIL.Image.Image image mode=RGB size=368x674>,
   'ID': 'Nassimi',
   'Strict_flag': False,
   'age': None,
   'gender': None,
   'emotion': None},
  {'Face_coordination': (1494, 194, 1573, 312),
   'Face_image': <PIL.Image.Image image mode=RGB size=79x118>,
   'Body_coordination': (1405, 194, 1579, 578),
   'Body_image': <PIL.Image.Image image mode=RGB size=174x384>,
   'ID': None,
   'Strict_flag': False,
   'age': None,
   'gender': None,
   'emotion': None},
  True]]
```

## License
Person Verification is open-sourced under the MIT License. See [LICENSE](LICENSE) for more details.

## Contributing
While we deeply value community input and interest in Person Verification, the project is currently in a phase where we're mapping out our next steps and are not accepting contributions just yet. We are incredibly grateful for your support and understanding. Please stay tuned for future updates when we'll be ready to welcome contributions with open arms.

## Credits and Acknowledgements
We would like to extend our heartfelt thanks to Mr.Poorya Aghaomeedi for his guidance and wisdom throughout the development of Person Verification. His insights have been a beacon of inspiration for this project.

## Contact Information
Although we're not open to contributions at the moment, your feedback and support are always welcome. Please feel free to star the project or share your thoughts through the Issues tab on GitHub, and we promise to consider them carefully.please [open an issue](https://github.com/Amir-Nassimi/Person-Verification/issues) in the Person Verification repository, and we will assist you.