import os
import requests
from flask import request

from dproxy.config import Config


def post_rollout():
    data = request.get_json()

    # Post state updating
    payload = {"hostname": data["hostname"], "state": "updating"}
    r = requests.patch("{}/server".format(data["url"]), json=payload, verify=False)

