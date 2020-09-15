from dproxy.tasks.runner import make_runner
from dproxy.utils import install_pkgs, restart_service, sudo_cmd

import os
import requests
from flask import current_app, jsonify
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
runner = make_runner(current_app)


@runner.task(bind=True)
def server_update(self, data):
    logger.info("Starting Update for {}".format(data["hostname"]))
    try:
        headers = {"Authorization": "token"}
        r = requests.post("{}/update".format(data["url"]), headers=headers, json=data)
        return jsonify(r.get_json())
    except Exception as e:
        logger.error(e)


@runner.task(bind=True)
def proxy_update(self, data):
    logger.info("Starting Update for {}".format(data["hostname"]))
    try:
        for pkg in data["versionlock"]:
            sudo_cmd("yum versionlock add {}".format(pkg))
        install_pkgs(data["versionlock"])
        restart_service("dproxy.service")
    except Exception as e:
        logger.error(e)
