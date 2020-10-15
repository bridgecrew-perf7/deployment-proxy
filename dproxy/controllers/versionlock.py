import os
import base64
import requests
from flask import request
from dproxy.utils import get_http

def post_versionlock():
    data = request.get_json()
    http = get_http
    r = http.patch(f"{data['url']}/versionlock", json=data)
    resp = r.json()
    return resp, 201


def get_versionlock(url):
    url = url.decode("ascii")
    http = get_http
    r = http.patch(f"{url}/versionlock", json=data)
    resp = r.json()
    return resp, 201
