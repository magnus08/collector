import os

from flask import Flask
from flask import jsonify

from collector import collect
from collector.sensor import bme280_sensor
from collector.sensor import status


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

    @fapp.route('/status')
    def stat():
        return jsonify(status.status())

    fapp.run(debug=True, host='0.0.0.0')
