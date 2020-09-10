import os
import requests
from flask import request

from dproxy.config import Config


def start_rollback(data):
    "deployment_id"
    "hostname"
    "deployment_proxy_url"
    "url"
    "yum_transaction_id"
    "yum_rollback_id"
    "versionlock"
