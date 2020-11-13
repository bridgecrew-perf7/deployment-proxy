import requests
from flask import request
from dproxy.util.http_helper import get_http


def get_versionlock(hostname, port):
    try:
        http = get_http
        r = http.get(f"http://{hostname}:{port}/api/v1/versionlock", json=data)
        resp = r.json()
        return resp, 201
    except Exception as e:
        raise Exception(f"Unable to Get versionlock: {e}")
