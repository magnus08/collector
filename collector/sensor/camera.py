from collector.config import config

try:
    from picamera import PiCamera
except ImportError:
    PiCamera = None
    print("Camera not supported")

import time
from datetime import datetime


def snap():
    if PiCamera:
        with PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            time.sleep(5)

            filename = time.strftime("%Y%m%d-%H%M%S.jpg")
            camera.capture("{}/{}".format(config['image_store'], filename))
            camera.stop_preview()
            return {
                "filename": filename,
                "timestamp": datetime.now()
            }
    else:
        return {
            "filename": "",
            "timestamp": datetime.now()
        }
