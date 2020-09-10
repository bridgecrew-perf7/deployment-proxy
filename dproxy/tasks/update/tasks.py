import requests

from flask import current_app, jsonify
from dproxy.tasks.runner import make_runner

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
runner = make_runner(current_app)


@runner.task(bind=True)
def run_update(self, data):
    logger.info("Starting Update for {}".format(data["hostname"]))
    try:
        headers = {"Authorization": "token"}
        r = requests.post("{}/update".format(data["url"]), headers=headers, json=data)
        return jsonify(r.get_json())
    except Exception as e:
        logger.error(e)
