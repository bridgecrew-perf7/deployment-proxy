from dproxy.config import Config

import requests
from flask import current_app
from dproxy.tasks.runner import make_runner

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
runner = make_runner(current_app)


@runner.task(bind=True)
def server(self, data):
    logger.info("Patching server for {}".format(data["hostname"]))
    try:
        headers = {"Authorization": Config.TOKEN}
        requests.post("{}/server".format(Config.DEPLOYMENT_API_URI), headers=headers, json=data)
    except Exception as e:
        logger.error(e)


@runner.task(bind=True)
def server_history(self, data):
    logger.info("Posting Server History for {}".format(data["hostname"]))
    try:
        headers = {"Authorization": Config.TOKEN}
        requests.post("{}/server/history".format(Config.DEPLOYMENT_API_URI), headers=headers, json=data)
    except Exception as e:
        logger.error(e)
