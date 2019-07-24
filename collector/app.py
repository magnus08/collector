import os
import sqlite3
from datetime import datetime

import dateutil.parser
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_file

from collector import collect
from collector.sensor import bme280_sensor
from collector.sensor import camera
from collector.sensor import status

db_name = '/store/collector.db' # TODO: Share this

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
        # print(request.form["from"])
        if request.args.get('from'):
            from_date_str = request.args.get('from', '')
            from_date = dateutil.parser.parse(from_date_str)
            to_date_str = request.args.get('to', '')
            to_date = dateutil.parser.parse(to_date_str) if to_date_str else datetime.now()
            print("Date: {}".format(from_date_str))
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            cursor.execute("SELECT humidity, pressure, temperature, timestamp FROM bme WHERE timestamp BETWEEN (?) AND (?)",
                           (from_date.timestamp(), to_date.timestamp()))
            rows = cursor.fetchall()

            print("Rows {}".format(rows))
            r = [{
                "humidity": row[0],
                "pressure": row[1],
                "temperature": row[2],
                "timestamp": datetime.fromtimestamp(row[3]).isoformat()
            } for row in rows]

            cursor.connection.close()

            print(r)
            return jsonify(r)
        else:
            print("No date")
            return jsonify(bme280_sensor.poll())

    @fapp.route('/snap')
    def snap():
        print('Snapping image at %s' % datetime.now())
        v = camera.snap()
        return send_file(v["filename"])

    @fapp.route('/status')
    def stat():
        return jsonify(status.status())

    fapp.run(debug=True, host='0.0.0.0')
