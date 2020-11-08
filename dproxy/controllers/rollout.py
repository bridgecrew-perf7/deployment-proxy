from dproxy.tasks.deployment.tasks import rollout
from dproxy.tasks.watcher import Watcher

import os
from flask import request


def post_rollout():
    inventory = request.get_json()
    try:
        Watcher("rollout", inventory)
        response = {"status": "success", "message": "Rollout successfully started"}
        return response, 202
    except Exception as e:
        response = {
            "status": "failure",
            "message": "Rollout failed to start",
            "exception": str(e),
        }
        return response, 409
