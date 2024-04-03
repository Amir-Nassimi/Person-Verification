# Django Camera Streaming and Person Detection Project

This project is a Django application that streams video from cameras and detects persons in the video stream or from an image file. The application is containerized using Docker and orchestrated with Docker Compose.

## Prerequisites

- Docker

## Getting Started

1. Clone the repository:
    ```
    https://github.com/Amir-Nassimi/Person-Verification.git
    ```
2. Navigate to the project directory:
    ```
    backend_face_verification
    ```
3. Clone the repository:
    ```
    http://172.16.16.41:8080/tfs/tnc_itc/Meta%20Intelligence/_git/person_verification
    ```
4. Build and run the Docker containers:
    ```
    docker compose up --build
    ```
The application should now be running at `http://0.0.0.0:8000`.

## Usage

- **Person Detection**: Upload an image file or provide a camera feed, and the application will detect persons in the image or video stream.

## Contributing

Please read `person_verification/README.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.