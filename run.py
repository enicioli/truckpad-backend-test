#!/usr/bin/env python

import logging
from flask_cors import CORS
from flask import Flask, jsonify

from config._abstract import AbstractConfig
from api.routes.trucker import TruckerController
from api.routes.check_in import CheckInController

app = Flask(__name__)
app.config.from_object(AbstractConfig.get_config_class())
app.register_blueprint(TruckerController)
app.register_blueprint(CheckInController)

AbstractConfig.set_up_db()

CORS(app)


@app.route("/", methods=['GET'])
def route_index():
    return jsonify({
        'apiVersion': 1.0
    })


@app.errorhandler(KeyError)
def handle_key_error(error):
    return jsonify({'error': str(error)}), 500


@app.errorhandler(Exception)
def handle_exception(error):
    logging.warning('Error happened in request: {}'.format(str(error)))

    from json import JSONDecodeError
    if isinstance(error, JSONDecodeError):
        return jsonify({'message': 'Bad request'}), 400

    from pymongo.errors import PyMongoError
    if isinstance(error, PyMongoError):
        return jsonify({'message': str(error)}), 400

    import traceback
    traceback.print_exc()
    error = {'message': str(error), 'type': str(type(error).__name__)}
    return jsonify({'error': error}), 500


@app.before_first_request
def setup_logging():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
