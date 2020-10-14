#!/usr/bin/python3
from dproxy.utils import update_env
from dproxy.tasks.runner import make_runner
from dproxy.config import Config, get_logger, get_proxies

import os
import requests
import connexion
from flask import Flask, request

logger = get_logger()
proxies = get_proxies()

if not Config.TOKEN:
    data = {
        "created_by": "dproxy",
        "hostname": Config.HOSTNAME,
        "ip": Config.IP,
        "state": Config.STATE,
        "location": Config.LOCATION,
        "environment": Config.ENVIRONMENT,
        "url": Config.DEPLOYMENT_PROXY_URI
    }
    if Config.USE_PROXIES:
        r = requests.post("{}/register/proxy".format(Config.DEPLOYMENT_API_URI), proxies=proxies, json=data)
    else:
        r = requests.post("{}/register/proxy".format(Config.DEPLOYMENT_API_URI), json=data)
    resp = r.json()
    logger.info(resp)
    if "token" in resp:
        update_env("STATE", "ACTIVE")
        update_env("TOKEN", resp["token"])
        os.environ["STATE"] = "ACTIVE"
        os.environ["TOKEN"] = resp["token"]
        
flask_app = connexion.FlaskApp(__name__)
flask_app.add_api("openapi.yaml", validate_responses=True, strict_validation=True)
app = flask_app.app
app.config.from_object(Config)
with app.app_context():
    runner = make_runner(app)
