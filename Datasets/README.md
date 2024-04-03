## Features

This folder contains dataset for the face verification task.
* representations_facenet512.pkl -> It is the main dataset for all the people work in the 3rd floor. Moreover, it is a pickle file consisting of people family name as keys and feature vectors as values. Each person has at least one, and at most five feature vectors. This is the main file that we use in our code.
* representations_facenet512_old.pkl -> This pickle file is almost similar to the previous one. However, the keys are the address for image files.
* Fix_face_dataset.ipynb -> This is a jupyter notebook file that helps us to convert 'representations_facenet512_old.pkl' to 'representations_facenet512.pkl'.

