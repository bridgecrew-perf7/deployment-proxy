import os
import requests
from flask import request

from dproxy.config import Config, get_logger, get_proxies
logger = get_logger()
proxies = get_proxies


def post_register_server():
    data = request.get_json()
    try:
        logger.info(f"POST REGISTER SERVER: {data}")
        r = requests.post(f"{Config.DEPLOYMENT_API_URI}/register/server", json=data)
        resp = r.json()
        logger.info(f"RESPONSE REGISTER SERVER: {resp}")
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
