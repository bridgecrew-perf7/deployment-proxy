import os
from flask import request

from dproxy.util.config import Config
from dproxy.tasks.deployment.tasks import rollback
from dproxy.tasks.watcher import Watcher


def post_rollback():
    inventory = request.get_json()
    try:
        tasks = []
        for host in inventory["hosts"]:
            tasks.append(rollback.s(host))
        Watcher(tasks)
        response = {
            "status": "success",
            "message": "Rollback successfully started",
        }
        return response, 202
    except Exception as e:
        response = {
            "status": "failure",
            "message": "Rollback failed to start",
            "exception": str(e)
        }
        return response, 409
