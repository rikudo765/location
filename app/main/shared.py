import os
import logging
from google.cloud import logging as gcplog

VERSION = "1.0"
logger = logging.getLogger("cloudLogger")


def init_shared(test_mode):
    global VERSION
    global logger

    if not test_mode:
        VERSION += ".{}".format(os.getenv("VERSION_TAG"))
        logger.addHandler(gcplog.Client().get_default_handler())
        logger.setLevel(level=logging.INFO)
    else:
        VERSION += ".local"
        logger.setLevel(level=logging.DEBUG)
