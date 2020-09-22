from dproxy.config import Config
from dproxy.config import get_logger

import os
import requests
from flask import request

logger = get_logger()


def patch_server():
    data = request.get_json()

    cookies = {"access_token_cookie": request.headers["Authorization"]}
    r = requests.patch(Config.DEPLOYMENT_API_URI + "/server/hostname/" + data["hostname"], cookies=cookies, json=data)
    resp = r.json()
    logger.info(resp)
    return resp, 201


def post_server_history():
    data = request.get_json()

    cookies = {"access_token_cookie": request.headers["Authorization"]}
    r = requests.post(Config.DEPLOYMENT_API_URI + "/server/history", cookies=cookies, json=data)
    resp = r.json()
    logger.info(resp)
    return resp, 201
