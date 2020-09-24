import os
import base64
import requests
from flask import request

from dproxy.config import Config


def post_versionlock():
    data = request.get_json()

    # POST to dclient url
    r = requests.patch(data["url"] + "/versionlock", json=data)
    resp = r.json()
    return resp, 201


def get_versionlock(url):

    url = url.decode("ascii")
    r = requests.patch(url + "/versionlock", json=data)
    resp = r.json()
    return resp, 201
