import os
import requests
from flask import request

from dproxy.config import Config


def post_versionlock():
    data = request.get_json()

    response = {
        "status": "success",
        "message": "Versionlock successfully updated",
    }
    return response, 201


def get_versionlock():

    response = {
        "status": "success",
        "message": "Rollback successfully started",
        "versionlock": versionlock
    }
    return response, 200
