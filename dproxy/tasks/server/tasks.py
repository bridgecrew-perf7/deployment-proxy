from dproxy.util.http_helper import get_http
from dproxy.util.config import Config

from flask import current_app, request
from dproxy.tasks.runner import make_runner
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
runner = make_runner(current_app)


@runner.task(bind=True)
def server(self, data):
    logger.info(f"Patching server for {data['hostname']}")
    try:
        cookies = {"access_token_cookie": request.headers["Authorization"]}
        http = get_http
        http.patch(f"{Config.DEPLOYMENT_API_URI}/server", cookies=cookies, json=data)
    except Exception as e:
        logger.error(e)


@runner.task(bind=True)
def server_history(self, data):
    logger.info(f"Posting Server History for {data['hostname']}")
    try:
        cookies = {"access_token_cookie": request.headers["Authorization"]}
        http = get_http
        http.post(
            f"{Config.DEPLOYMENT_API_URI}/server/history", cookies=cookies, json=data
        )
    except Exception as e:
        logger.error(e)
