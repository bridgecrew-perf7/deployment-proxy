import os
import requests
from flask import request

from dproxy.config import Config


def patch_server():
    data = request.get_json()
    
    response = {
        "status": "success",
        "message": "Server successfully patched",
    }
    return response, 204


def post_server_history():
    data = request.get_json()

    response = {
        "status": "success",
        "message": "Server History successfully updated",
    }
    return response, 204
