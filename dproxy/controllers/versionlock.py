import requests
from flask import request
from dproxy.util.http_helper import get_http


def post_versionlock():
    data = request.get_json()
    r = requests.post(f"{data['url']}/versionlock", json=data)
    resp = r.json()
    return resp, 201


def get_versionlock(url):
    url = url.decode("ascii")
    http = get_http
    r = http.get(f"{url}/versionlock", json=data)
    resp = r.json()
    return resp, 201
