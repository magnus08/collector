from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from collector.sensor import bme280_sensor
from collector.sensor import camera
from collector.sensor import status
import sqlite3

db_name = '/store/collector.db'


def poll_bme280():
    print('Polling bme280 at %s' % datetime.now())

    v = bme280_sensor.poll();
    print('bme values = %s' % v)
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute('''INSERT INTO bme(humidity, pressure, temperature, timestamp) VALUES(?, ?, ?, ?)''', (v["humidity"], v["pressure"], v["temperature"], v["timestamp"].timestamp()))
    db.commit()


def snap_image():
    print('Snapping image at %s' % datetime.now())
    v = camera.snap()
    print('snap values = %s' % v)
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute('''INSERT INTO camera(filename, timestamp) VALUES(?, ?)''',
                   (v["filename"], v["timestamp"].timestamp()))
    db.commit()


def collect_status():
    print('Collecting status %s' % datetime.now())
    v = status.status()
    print('status values = %s' % v)
    db = sqlite3.connect(db_name)
    cursor = db.cursor()

    cursor.execute('''INSERT INTO status(size, free, timestamp) VALUES(?, ?, ?)''',
                   (v["size"], v["free"], v["timestamp"].timestamp()))
    db.commit()


def start():
    print("Starting up")

    scheduler = BackgroundScheduler()
    scheduler.add_job(poll_bme280, 'interval', seconds=15)
    scheduler.add_job(collect_status, 'interval', seconds=10)
    scheduler.add_job(snap_image, 'interval', seconds=60)
    scheduler.start()
