from dproxy.tasks.deployment.tasks import rollback
from dproxy.tasks.watcher import Watcher

import os
from flask import request


def post_rollback():
    inventory = request.get_json()
    try:
        Watcher("rollback", inventory)
        response = {
            "status": "success",
            "message": "Rollback successfully started"
        }
        return response, 202
    except Exception as e:
        response = {
            "status": "failure",
            "message": "Rollback failed to start",
            "exception": str(e)
        }
        return response, 409
