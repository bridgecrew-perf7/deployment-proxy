#!/usr/bin/python3
from dproxy.util.config import Config
from dproxy.tasks.runner import make_runner
from dproxy.util.core import set_state, register_proxy

import os
import connexion

import logging.handlers

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
)

rotating_log_handeler = logging.handlers.RotatingFileHandler(
    Config.LOG_FILE,
    maxBytes=int(Config.LOG_MAX_BYTES),
    backupCount=int(Config.LOG_BACKUP_COUNT),
)
rotating_log_handeler.setFormatter(formatter)
rotating_log_handeler.setLevel(logging.DEBUG)
logging.getLogger("").addHandler(rotating_log_handeler)


flask_app = connexion.FlaskApp(__name__)
flask_app.add_api("openapi.yaml", validate_responses=True, strict_validation=True)
app = flask_app.app
app.config.from_object(Config)
with app.app_context():
    runner = make_runner(app)
    if not os.getenv("TOKEN"):
        register_proxy(app)
    else:
        set_state(app, "ACTIVE")
