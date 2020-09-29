from dproxy.config import Config
from dproxy.config import get_logger, get_proxies

import os
import requests
from flask import request

logger = get_logger()
proxies = get_proxies()


def patch_server():
    data = request.get_json()
    cookies = {"access_token_cookie": request.headers["Authorization"]}
    r = requests.patch(f"{Config.DEPLOYMENT_API_URI}/server/hostname/{data['hostname']}", proxies=proxies, 
                       cookies=cookies, json=data)
    resp = r.json()
    return resp, 201


def post_server_history():
    data = request.get_json()

    cookies = {"access_token_cookie": request.headers["Authorization"]}
    r = requests.post(f"{Config.DEPLOYMENT_API_URI}/server/history", proxies=proxies, cookies=cookies, json=data)
    resp = r.json()
    return resp, 201
