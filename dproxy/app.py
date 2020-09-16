#!/usr/bin/python3

from dproxy.config import Config
from dproxy.tasks.runner import make_runner
from dproxy.controllers.rollout import post_rollout
from dproxy.controllers.rollback import post_rollback
from dproxy.controllers.versionlock import post_versionlock
from dproxy.controllers.healthcheck import get_healthcheck
from dproxy.controllers.server import patch_server, post_server_history

import requests
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
        with open("/etc/default/dproxy", "a") as file:
            file.write("TOKEN={}".format(resp["token"]))


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/", methods=["GET", "POST"])
def healthcheck():
    if request.method == "GET":
        return get_healthcheck()


@app.route("/rollout", methods=["POST"])
def rollout():
    if request.method == "POST":
        return post_rollout()


@app.route("/rollback", methods=["POST"])
def rollback():
    if request.method == "POST":
        return post_rollback()


@app.route("/server", methods=["PATCH"])
def server():
    if request.method == "PATCH":
        return patch_server()


@app.route("/server/history", methods=["POST"])
def server_history():
    if request.method == "POST":
        return post_server_history()


@app.route("/versionlock", methods=["POST"])
def versionlock():
    if request.method == "POST":
        return post_versionlock()


@app.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        return post_update()
    

with app.app_context():
    runner = make_runner(app)
