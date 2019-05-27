from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from collector.sensor import bme280_sensor
from collector.sensor import camera
from collector.sensor import status


def poll_bme280():
    print('Polling bme280 at %s' % datetime.now())
    print(bme280_sensor.poll())


def snap_image():
    print('Snapping image at %s' % datetime.now())
    print(camera.snap())


def collect_status():
    print('Collecting status %s' % datetime.now())
    print(status.status())


def start():
    print("Starting up")

    scheduler = BackgroundScheduler()
    scheduler.add_job(poll_bme280, 'interval', seconds=15)
    scheduler.add_job(collect_status, 'interval', seconds=10)
    scheduler.add_job(snap_image, 'interval', seconds=60)
    scheduler.start()
