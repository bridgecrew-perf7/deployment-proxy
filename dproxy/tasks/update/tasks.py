from dproxy.tasks.runner import make_runner
from dproxy.util.http_helper import get_http
from dproxy.util.core import restart_service, install_pkgs

import os
import requests
from flask import current_app, jsonify
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
runner = make_runner(current_app)


@runner.task(bind=True)
def server_update(self, data):
    logger.info(f"Starting Update for {data['hostname']}")
    try:
        http = get_http
        r = http.post(f"{data['url']}/update", json=data)
        return jsonify(r.get_json())
    except Exception as e:
        logger.error(e)


@runner.task(bind=True)
def proxy_update(self, data):
    logger.info(f"Starting Update for {data['hostname']}")
    try:
        os.system("pip3 install --upgrade dproxy")
        restart_service("dproxy.service")
    except Exception as e:
        logger.error(e)
