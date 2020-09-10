from dproxy.config import Config
from dproxy.tasks.update.tasks import server_update

import os
import requests
from flask import request


def post_update():
    data = request.get_json()
    try:
        if data["hostname"] == Config.HOSTNAME:
            proxy_update.apply_async(args=[data])
        else:
            server_update.apply_async(args=[data])
        response = {
            "status": "success",
            "message": "Server update started",
        }
        return response, 204
    except Exception as e:
        response = {
            "status": "failure",
            "message": "Server update failed",
            "exception": str(e)
        }
        return response, 409
