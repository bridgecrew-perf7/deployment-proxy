import os
import requests
from flask import request

from dproxy.config import Config
from dproxy.tasks.deployment.task import rollback


def post_rollback():
    data = request.get_json()

    try:
        rollback.apply_async(args=[data])
        response = {
            "status": "success",
            "message": "Rollback successfully started",
        }
        return response, 204
    except Exception as e:
        response = {
            "status": "failure",
            "message": "Rollback failed to start",
            "exception": str(e)
        }
        return response, 409
