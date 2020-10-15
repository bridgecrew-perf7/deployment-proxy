from dproxy.config import Config, get_logger
from dproxy.utils import get_http

import os
from flask import request

logger = get_logger()


def patch_server():
    data = request.get_json()
    cookies = {"access_token_cookie": request.headers["Authorization"]}
    http = get_http
    r = http.patch(f"{Config.DEPLOYMENT_API_URI}/server/hostname/{data['hostname']}", cookies=cookies, json=data, 
                       verify=False)
    resp = r.json()
    return resp, 201


def post_server_history():
    data = request.get_json()
    cookies = {"access_token_cookie": request.headers["Authorization"]}
    http = get_http
    r = http.post(f"{Config.DEPLOYMENT_API_URI}/server/history", cookies=cookies, json=data, verify=False)
    resp = r.json()
    return resp, 201
