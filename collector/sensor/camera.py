#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Full credit to https://github.com/IDCFChannel/bme280-meshblu-py (or who ever
originally wrote bme280_sample.py)
"""

try:
    from picamera import PiCamera
except ImportError:
    PiCamera = None
    print("Camera not supported")

import time


def snap():
    if PiCamera:
        with PiCamera() as camera:
            camera.start_preview()
            time.sleep(5)

            filename = time.strftime("%Y%m%d-%H%M%S.jpg")
            camera.capture(filename)
            camera.stop_preview()
            return filename
    else:
        return ""