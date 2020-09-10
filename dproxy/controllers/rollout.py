import os
import requests
from flask import request

from dproxy.config import Config
from dproxy.tasks.deployment.task import rollout


def post_rollout():
    data = request.get_json()

    try:
        rollout.apply_async(args=[data])
        response = {
            "status": "success",
            "message": "Rollout successfully started",
        }
        return response, 204
    except Exception as e:
        response = {
            "status": "failure",
            "message": "Rollout failed to start",
            "exception": str(e)
        }
        return response, 409
