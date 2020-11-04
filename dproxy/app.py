#!/usr/bin/python3
from dproxy.util.config import Config
from dproxy.util.logger import get_logger
from dproxy.tasks.runner import make_runner
from dproxy.util.core import set_state, register_proxy

import os
import requests
import connexion
from dotenv import load_dotenv
from flask import Flask, request


if not os.getenv("TOKEN"):
    register_proxy()
else:
    set_state("ACTIVE")


flask_app = connexion.FlaskApp(__name__)
flask_app.add_api("openapi.yaml", validate_responses=True, strict_validation=True)
app = flask_app.app
app.config.from_object(Config)
with app.app_context():
    runner = make_runner(app)
