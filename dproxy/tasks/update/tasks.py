from dproxy.config import get_proxies
from dproxy.tasks.runner import make_runner
from dproxy.utils import install_pkgs, restart_service

import os
import requests
from flask import current_app, jsonify
from celery.utils.log import get_task_logger

proxies = get_proxies()
logger = get_task_logger(__name__)
runner = make_runner(current_app)


@runner.task(bind=True)
def server_update(self, data):
    logger.info(f"Starting Update for {data['hostname']}")
    try:
        cookies = {"access_token_cookie": request.headers["Authorization"]}
        r = requests.post(f"{data['url']}/update", cookies=cookies, json=data)
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
