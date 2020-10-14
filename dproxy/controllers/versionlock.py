import os
import base64
import requests
from flask import request


def post_versionlock():
    data = request.get_json()
    r = requests.patch(f"{data['url']}/versionlock", json=data)
    resp = r.json()
    return resp, 201


def get_versionlock(url):
    url = url.decode("ascii")
    r = requests.patch(f"{url}/versionlock", json=data)
    resp = r.json()
    return resp, 201
