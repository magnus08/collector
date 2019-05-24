import time
from datetime import datetime
from collector.sensor import bme280_sensor

from apscheduler.schedulers.background import BackgroundScheduler


def tick():
    print('Tick! The time is: %s' % datetime.now())
    print(bme280_sensor.poll())


def start():
    print("Starting up")

    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down")
        scheduler.shutdown()
