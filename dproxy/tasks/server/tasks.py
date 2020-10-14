import requests
from flask import current_app
from dproxy.tasks.runner import make_runner
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
runner = make_runner(current_app)


@runner.task(bind=True)
def server(self, data):
    logger.info(f"Patching server for {data['hostname']}")
    try:
        cookies = {"access_token_cookie": request.headers["Authorization"]}
        requests.post(f"{Config.DEPLOYMENT_API_URI}/server", cookies=cookies, json=data, verify=False)
    except Exception as e:
        logger.error(e)


@runner.task(bind=True)
def server_history(self, data):
    logger.info(f"Posting Server History for {data['hostname']}")
    try:
        cookies = {"access_token_cookie": request.headers["Authorization"]}
        requests.post(f"{Config.DEPLOYMENT_API_URI}/server/history", cookies=cookies, json=data, verify=False)
    except Exception as e:
        logger.error(e)
