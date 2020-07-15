import os
from flask import Flask
from app.main.shared import logger, VERSION, init_shared
from app.main.api import handler
from app.main.globals import storage


def create_app():
    test_mode = not (os.getenv('TEST_MODE') is None)

    init_shared(test_mode)
    storage.init_app(test_mode)
    logger.info("starting location service, test_mode={}, VERSION={}".format(test_mode, VERSION))

    location_app = Flask(__name__)
    if test_mode:
        location_app.debug = True

    location_app.register_blueprint(handler)

    return location_app
