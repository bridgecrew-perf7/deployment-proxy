from dproxy.config import get_proxies

import os
import base64
import requests
from flask import request


def post_versionlock():
    data = request.get_json()
    r = requests.patch(f"{data['url']}/versionlock", proxies=proxies, json=data)
    resp = r.json()
    return resp, 201


def get_versionlock(url):
    url = url.decode("ascii")
    r = requests.patch(f"{url}/versionlock", proxies=proxies, json=data)
    resp = r.json()
    return resp, 201
