from dproxy.config import Config
from dproxy.tasks.update.tasks import server_update
from dproxy.tasks.watcher import Watcher

import os
import requests
from flask import request


def post_update():
    inventory = request.get_json()
    try:
        if "hosts" in inventory:
            Watcher("server_update", inventory)
        elif "hostname" in data and data["hostname"] == Config.HOSTNAME:
            proxy_update.apply_async(args=[data])
        response = {
            "status": "success",
            "message": "Server update started",
        }
        return response, 202
    except Exception as e:
        response = {
            "status": "failure",
            "message": "Server update failed",
            "exception": str(e)
        }
        return response, 409
