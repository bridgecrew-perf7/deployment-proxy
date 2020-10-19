import os
import socket
import logging
from dotenv import load_dotenv

ENV_FILE = os.getenv("ENV_FILE")
load_dotenv(ENV_FILE)


def get_env(var):
    if os.getenv(var):
        return os.getenv(var)
    else:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        default = {
            "ENV_FILE": "/etc/default/dproxy",
            "HOSTNAME": hostname,
            "IP": ip,
            "STATE": "NEW",
            "LOCATION": "PROVO",
            "ENVIRONMENT": "PRODUCTION",
            "DEPLOYMENT_PROXY_URI": f"http://{hostname}:8002/api/1.0.0",
            "DEPLOYMENT_API_URI": "https://deployment.unifiedlayer.com/api/1.0.0",
            "RETRY": 10,
            "TOKEN": None
        }
        return default[var]


class Config(object):
    HOSTNAME = get_env("HOSTNAME")
    IP = get_env("IP")
    STATE = get_env("STATE")
    LOCATION = get_env("LOCATION")
    ENVIRONMENT = get_env("ENVIRONMENT")
    DEPLOYMENT_PROXY_URI = get_env("DEPLOYMENT_PROXY_URI")
    DEPLOYMENT_API_URI = get_env("DEPLOYMENT_API_URI")
    ENV_FILE = get_env("ENV_FILE")
    RETRY = get_env("RETRY")
    TOKEN = get_env("TOKEN")

    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    CELERY_TASK_SERIALIZER = os.getenv("CELERY_TASK_SERIALIZER")
    CELERY_RESULT_SERIALIZER = os.getenv("CELERY_RESULT_SERIALIZER")
    CELERY_ACCEPT_CONTENT = os.getenv("CELERY_ACCEPT_CONTENT")
    CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE")
    CELERY_UTC = os.getenv("CELERY_UTC")


def get_logger():
    logger = logging.getLogger("bhdapi")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("/var/log/deployment/dproxy.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
