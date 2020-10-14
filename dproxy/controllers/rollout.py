from dproxy.tasks.deployment.tasks import rollout

import os
from flask import request


def post_rollout():
    data = request.get_json()
    try:
        rollout.apply_async(args=[data])
        response = {
            "status": "success",
            "message": "Rollout successfully started",
        }
        return response, 202
    except Exception as e:
        response = {
            "status": "failure",
            "message": "Rollout failed to start",
            "exception": str(e)
        }
        return response, 409
