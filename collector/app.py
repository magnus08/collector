from collector import collect
import os
from flask import Flask
from flask import jsonify

from collector.sensor import bme280_sensor


def run():
    collect.start()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'collect.sqlite')
    )

    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/sensor')
    def hello():
        return jsonify(bme280_sensor.poll())


    app.run(debug=True, host='0.0.0.0')
