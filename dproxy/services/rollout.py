import os
import requests
from flask import request

from dproxy.config import Config


def post_rollout():
    data = request.get_json()
    pass

