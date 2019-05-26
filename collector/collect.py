import time
from datetime import datetime
from collector.sensor import bme280_sensor
from collector.sensor import camera

from apscheduler.schedulers.background import BackgroundScheduler


def poll_bme280():
    print('Polling bme280 at %s' % datetime.now())
    print(bme280_sensor.poll())


def snap_image():
    print('Snapping image at %s' % datetime.now())
    print(camera.snap())


def start():
    print("Starting up")

    scheduler = BackgroundScheduler()
    scheduler.add_job(poll_bme280, 'interval', seconds=15)
    scheduler.add_job(snap_image, 'interval', seconds=60)
    scheduler.start()

    # try:
    #     # This is here to simulate application activity (which keeps the main thread alive).
    #     while True:
    #         time.sleep(2)
    # except (KeyboardInterrupt, SystemExit):
    #     print("Shutting down")
    #     scheduler.shutdown()
