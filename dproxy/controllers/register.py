import os
import requests
from flask import request

from dproxy.config import Config


def post_register_server():
    data = request.get_json()

    #try:
    r = requests.post(Config.DEPLOYMENT_SERVER_URL + "/register/server", json=data)
    print(r.content)
    resp = r.json()
    response = {
        "status": "success",
        "message": "Server successfully registered",
        "TOKEN": resp["TOKEN"]
    }
    return response, 204
    #except Exception as e:
    #    response = {
    #        "status": "failure",
    #        "message": "Register server failed",
    #        "exception": str(e)
    #    }
    #    return response, 409
