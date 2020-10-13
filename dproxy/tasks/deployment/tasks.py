from dproxy.config import Config, get_proxies
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
            r = requests.get(f"{host['url']}/")
            status_codes.append({"hostname": host["hostname"], "status": r.status_code})
        return status_codes
    except Exception as e:
        logger.error(e)
        return False


@runner.task(bind=True)
def rollout(self, data=None, callback=None):
    logger.info(f"Starting Rollout for {data['hostname']}")
    r = requests.post(f"{data['url']}/rollout", json=data)
    result = r.json()
    if callback is not None:
        subtask(callback).delay(result)
    return result


@runner.task(bind=True)
def rollback(self, data=None, callback=None):
    logger.info(f"Starting Rollback for {data['hostname']}")
    r = requests.post(f"{data['url']}/rollback", json=data)
    result = r.json()
    if callback is not None:
        subtask(callback).delay(result)
    return result


@runner.task(bind=True)
def complete(self, results, deployment_id=None):
    logger.info("TASKS COMPLETED", results)
    cookies = {"access_token_cookie": Config.TOKEN}
    requests.post(f"{Config.DEPLOYMENT_API_URI}/deployment/results/{deployment_id}", cookies=cookies, json=results)
