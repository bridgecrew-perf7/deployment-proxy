import requests
from flask import request
from dproxy.util.http_helper import get_http


def get_versionlock(protocol, hostname, port, version):
    try:
        http = get_http
        r = http.get(f"{protocol}://{hostname}:{port}/api/{version}/versionlock", json=data)
        resp = r.json()
        return resp, 201
    except Exception as e:
        raise Exception(f"Unable to Get versionlock: {e}")
