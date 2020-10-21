from dproxy.util.config import Config
from dproxy.util.logger import get_logger
from dproxy.util.http_helper import get_http

import os
from flask import request

logger = get_logger()


def post_register_server():
    data = request.get_json()
    try:
        logger.debug(f"POST REGISTER SERVER: {data}")
        http = get_http()
        r = http.post(f"{Config.DEPLOYMENT_API_URI}/register/server", json=data)
        resp = r.json()
        logger.debug(f"RESPONSE REGISTER SERVER: {resp}")
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
