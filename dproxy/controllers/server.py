from dproxy.util.config import Config
from dproxy.util.logger import get_logger

import os
import requests
from flask import request

logger = get_logger()


def patch_server():
    data = request.get_json()
    cookies = {"access_token_cookie": request.headers["Authorization"]}
    r = requests.patch(f"{Config.DEPLOYMENT_API_URI}/server/hostname/{data['hostname']}", cookies=cookies, json=data)
    resp = r.json()
    logger.info(f"Updated Server: {resp} {r.status_code}")
    return resp, r.status_code


def post_server_history():
    data = request.get_json()
    cookies = {"access_token_cookie": request.headers["Authorization"]}
    http = get_http
    r = http.post(f"{Config.DEPLOYMENT_API_URI}/server/history", cookies=cookies, json=data)
    resp = r.json()
    return resp, r.status_code
