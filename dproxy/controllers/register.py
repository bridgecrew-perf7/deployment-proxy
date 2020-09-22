import os
import requests
from flask import request

from dproxy.config import Config
from dproxy.config import get_logger
logger = get_logger

def post_register_server():
    data = request.get_json()
    print(data)
    try:
        r = requests.post(Config.DEPLOYMENT_API_URI + "/register/server", json=data)
        logger.debug(r.content)
        resp = r.json()
        response = {
            "status": "success",
            "message": "Server successfully registered",
            "token": resp["token"]
        }
        return response, 200
    except Exception as e:
        response = {
            "status": "failure",
            "message": "Register server failed",
            "exception": str(e)
        }
        return response, 409