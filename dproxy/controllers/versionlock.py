import base64
import requests
from flask import request
from dproxy.util.http_helper import get_http


def post_versionlock():
    data = request.get_json()
    try:
        if "url" in data:
            url = base64.b64decode(data["url"])
            r = requests.post(f"{url}/versionlock", json=data)
            resp = r.json()
            return resp, 201
        else:
            response = {
                "status": "failed",
                "message": "Unable to find Base64 encoded client url."
            }
            return response, 409
    except Exception as e:
        raise Exception(f"Unable to Post versionlock: {e}")


def get_versionlock(url):
    try:
        url = base64.b64decode(url)
        http = get_http
        r = http.get(f"{url}/versionlock", json=data)
        resp = r.json()
        return resp, 201
    except Exception as e:
        raise Exception(f"Unable to Get versionlock: {e}")
