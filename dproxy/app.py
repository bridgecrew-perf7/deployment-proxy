#!/usr/bin/python3
from dproxy.config import Config
from dproxy.config import update_env
from dproxy.tasks.runner import make_runner
from dproxy.controllers.rollout import post_rollout
from dproxy.controllers.rollback import post_rollback
from dproxy.controllers.versionlock import post_versionlock
from dproxy.controllers.healthcheck import get_healthcheck
from dproxy.controllers.server import patch_server, post_server_history

import requests
import connexion
from flask import Flask, request


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
    r = requests.post("https://deployment.unifiedlayer.com/api/1.0.0/register/proxy", json=data, verify=False)
    resp = r.json()
    if "token" in resp:
        update_env("TOKEN", resp["token"])
        update_env("STATE", "ACTIVE")
        
        
flask_app = connexion.FlaskApp(__name__)
flask_app.add_api("openapi.yaml", validate_responses=True, strict_validation=True)
app = flask_app.app
app.config.from_object(Config)
with app.app_context():
    runner = make_runner(app)
