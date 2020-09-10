import os
import requests
from flask import request

from dproxy.config import Config
from dproxy.services.rollback import start_rollback

def post_rollback():
    data = request.get_json()

    try:
        rollback = start_rollback(data)
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
