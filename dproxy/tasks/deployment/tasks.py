from dproxy.tasks.runner import make_runner
from dproxy.util.http_helper import get_http

import base64
import requests
from flask import current_app
from celery import subtask
from celery.utils.log import get_task_logger
from dproxy.util.config import Config

logger = get_task_logger(__name__)
runner = make_runner(current_app)


def health_check(hosts):
    try:
        status_codes = []
        for host in hosts:
            http = get_http
            r = http.get(f"http://{host['hostname']}:{host['port']}/")
            status_codes.append(
                {
                    "hostname": host["hostname"],
                    "port": host["port"],
                    "status": r.status_code,
                }
            )
        return status_codes
    except Exception as e:
        logger.error(e)
        return False


@runner.task(bind=True)
def rollout(self, data=None, callback=None):
    logger.info(f"Starting Rollout for {data['hostname']}")
    http = get_http
    r = http.post(f"http://{data['hostname']}:{data['port']}/rollout", json=data)
    result = r.json()
    if callback is not None:
        subtask(callback).delay(result)
    return result


@runner.task(bind=True)
def rollback(self, data=None, callback=None):
    logger.info(f"Starting Rollback for {data['hostname']}")
    http = get_http

    r = http.post(f"http://{data['hostname']}:{data['port']}/rollback", json=data)

    result = r.json()
    if callback is not None:
        subtask(callback).delay(result)
    return result


@runner.task(bind=True)
def complete(self, results, deployment_id=None):
    logger.info("TASKS COMPLETED", results)
    cookies = {"access_token_cookie": Config.TOKEN}
    http = get_http
    http.post(
        f"{Config.DEPLOYMENT_API_URI}/deployment/results/{deployment_id}",
        cookies=cookies,
        json=results,
    )
