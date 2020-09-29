from dproxy.config import get_proxies
from dproxy.tasks.runner import make_runner

import requests
from flask import current_app
from celery import subtask
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
runner = make_runner(current_app)
proxies = get_proxies()


def health_check(hosts):
    try:
        status_codes = []
        for host in hosts:
            r = requests.get(f"{host['url']}/", proxies=proxies)
            status_codes.append({"hostname": host["hostname"], "status": r.status_code})
        return status_codes
    except Exception as e:
        logger.error(e)
        return False


@runner.task(bind=True)
def rollout(self, data, callback=None):
    logger.info(f"Starting Rollout for {data['hostname']}")
    r = requests.post(f"{data['url']}/rollout", proxies=proxies, json=data)
    result = r.json
    if callback is not None:
        subtask(callback).delay(result)
    return result


@runner.task(bind=True)
def rollback(self, data, callback=None):
    logger.info(f"Starting Rollback for {data['hostname']}")
    r = requests.post(f"{data['url']}/rollback", proxies=proxies, json=data)
    result = r.json
    if callback is not None:
        subtask(callback).delay(result)
    return result


@runner.task(bind=True)
def notify_complete(self, data, callback=None):
    logger.info(f"Notify complete for {data}")
