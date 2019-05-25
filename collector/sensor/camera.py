#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Full credit to https://github.com/IDCFChannel/bme280-meshblu-py (or who ever
originally wrote bme280_sample.py)
"""


from picamera import PiCamera
#from time import sleep
import time




def snap():
    camera = PiCamera()

    camera.start_preview()
    time.sleep(5)

    filename = time.strftime("%Y%m%d-%H%M%S.jpg")
    camera.capture(filename)
    camera.stop_preview()
    return filename
