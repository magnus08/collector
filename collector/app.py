from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import os


def tick():
    print('Tick! The time is: %s' % datetime.now())


def run():
    print("hello")

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
