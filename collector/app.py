import os
from datetime import datetime

from flask import Flask
from flask import jsonify
from flask import send_file

from collector import collect
from collector.sensor import bme280_sensor
from collector.sensor import status
from collector.sensor import camera


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
