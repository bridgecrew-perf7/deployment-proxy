import requests

from flask import current_app
from dproxy.tasks.runner import make_runner

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
runner = make_runner(current_app)


def health_check(hosts):
    try:
        status_codes = []
        for host in hosts:
            payload = {"hostname": host["hostname"], "healthcheck": "good"}
            r = requests.post(host["url"]+"/healthcheck", json=payload)
            status_codes.append({"hostname": host["hostname"], "status": r.status_code})
        return status_codes
    except Exception as e:
        print(e)
        return False


@runner.task(bind=True)
def rollout(self, data):
    logger.info("Starting Rollout for {}".format(data["hostname"]))
    try:
        headers = {"Authorization": "token"}
        requests.post("{}/rollout".format(data["deployment_proxy_url"]), headers=headers, json=data)
    except Exception as e:
        logger.error(e)


@runner.task(bind=True)
def rollback(self, data):
    logger.info("Starting Rollback for {}".format(data["hostname"]))
    try:
        headers = {"Authorization": "token"}
        requests.post("{}/rollback".format(data["deployment_proxy_url"]), headers=headers, json=data)
    except Exception as e:
        logger.error(e)
