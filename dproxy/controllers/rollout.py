import os
import requests
from flask import request

from dproxy.config import Config


def post_rollout():
    data = request.get_json()

    response = {
        "status": "success",
        "message": "Rollout successfully started",
    }
    return response, 204
