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

5. (Optional) Feel free to use our videos captured in an organization environment. To do so, please download and extract the videos in the following path via [this link](https://drive.google.com/drive/folders/1ybj9DcKsTv3HFFwVZfbNkCeaGhdoYC3c?usp=drive_link):

```bash
./Test/Samples/
```