from concurrent.futures import ThreadPoolExecutor

from celery import shared_task

from camera.camera_stream import camera_capture


@shared_task()
def camera_runner(max_workers, cameras):
    match max_workers:
        case 0:
            with ThreadPoolExecutor() as executor:
                executor.map(camera_capture, cameras)
        case _:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                executor.map(camera_capture, cameras)
