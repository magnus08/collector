import os
from datetime import datetime

import dateutil.parser
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_file

from collector import collect
from collector.db import get_db
from collector.sensor import bme280_sensor
from collector.sensor import camera
from collector.sensor import status
from collector.config import config

def get_range(request):
    if request.args.get('from'):
        from_date_str = request.args.get('from', '')
        from_date = dateutil.parser.parse(from_date_str)
        to_date_str = request.args.get('to', '')
        to_date = dateutil.parser.parse(to_date_str) if to_date_str else datetime.now()
        return from_date, to_date
    else:
        return None, None

def run():

    print("***Run")
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("***First startup")
        collect.start()

    fapp = Flask(__name__, instance_relative_config=True)
    fapp.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(fapp.instance_path, 'collect.sqlite')
    )

    fapp.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(fapp.instance_path)
    except OSError:
        pass

    @fapp.route('/sensor')
    def sensor():
        from_date, to_date = get_range(request)
        if from_date:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT humidity, pressure, temperature, timestamp FROM bme WHERE timestamp BETWEEN (?) AND (?)",
                           (from_date.timestamp(), to_date.timestamp()))
            rows = cursor.fetchall()
            cursor.connection.close()

            r = [{
                "humidity": row[0],
                "pressure": row[1],
                "temperature": row[2],
                "timestamp": datetime.fromtimestamp(row[3]).isoformat()
            } for row in rows]
            return jsonify(r)
        else:
            poll = bme280_sensor.poll()
            return jsonify({
                "humidity": poll["humidity"],
                "pressure": poll["pressure"],
                "temperature": poll["temperature"],
                "timestamp": poll["timestamp"].isoformat()
            })

    @fapp.route('/snap')
    def snap():
        print('Snapping image at %s' % datetime.now())
        v = camera.snap()
        return send_file(v["filename"])

    @fapp.route('/image/<filename>')
    @fapp.route('/image')
    def image(filename):
        if filename:
            full_filename = "{}/{}".format(config['image_store'], filename)
            return send_file(full_filename)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT filename, timestamp FROM camera ORDER BY timestamp DESC LIMIT 1")
            row = cursor.fetchone()

            cursor.connection.close()


    @fapp.route('/images')
    def images():
        from_date, to_date = get_range(request)
        if from_date:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT filename, timestamp FROM camera WHERE timestamp BETWEEN (?) AND (?)",
                           (from_date.timestamp(), to_date.timestamp()))
            rows = cursor.fetchall()
            print("+++ files = ", rows)
            cursor.connection.close()

            return jsonify([{
                "filename": row[0],
                "timestamp": datetime.fromtimestamp(row[1]).isoformat()
            } for row in rows])

    @fapp.route('/status')
    def stat():
        from_date, to_date = get_range(request)
        if from_date:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT size, free, timestamp FROM status WHERE timestamp BETWEEN (?) AND (?)",
                           (from_date.timestamp(), to_date.timestamp()))
            rows = cursor.fetchall()
            cursor.connection.close()

            return jsonify([{
                "size": row[0],
                "free": row[1],
                "timestamp": datetime.fromtimestamp(row[2]).isoformat()
            } for row in rows])
        else:
            res = status.status()
            return jsonify({
                "size": res["size"],
                "free": res["free"],
                "timestamp": res["timestamp"].isoformat()
            })

    fapp.run(debug=True, host='0.0.0.0')
