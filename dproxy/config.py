import os
import socket
import logging
from dotenv import load_dotenv


if os.getenv("ENV_FILE"):
    load_dotenv(os.getenv("ENV_FILE"))
elif os.path.exists(".env"):
    load_dotenv(".env")
    os.environ["ENV_FILE"] = ".env"
    ENV_FILE = ".env"
elif os.path.exists("/etc/default/dproxy"):
    load_dotenv("/etc/default/dproxy")
    os.environ["ENV_FILE"] = "/etc/default/dproxy"
    ENV_FILE = "/etc/default/dproxy"
else:
    print("UNABLE TO LOAD AN ENVIRONMENT FILE!")
    ENV_FILE = None


def get_env(var):
    if os.getenv(var):
        return os.getenv(var)
    else:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        default = {
            "HOSTNAME": hostname,
            "IP": ip,
            "STATE": "NEW",
            "LOCATION": "PROVO",
            "ENVIRONMENT": "PRODUCTION",
            "DEPLOYMENT_PROXY_URI": f"http://{hostname}:8002/api/1.0.0",
            "DEPLOYMENT_API_URI": "https://deployment.unifiedlayer.com/api/1.0.0",
            "RETRY": 10,
            "TOKEN": None,
            "DEFAULT_TIMEOUT": 5,
            "CELERY_BROKER_URL": "redis://localhost:6379/0",
            "CELERY_RESULT_BACKEND": "redis://localhost:6379/0",
            "CELERY_TASK_SERIALIZER": "json",
            "CELERY_RESULT_SERIALIZER": "json",
            "CELERY_ACCEPT_CONTENT": ["json", "application/text"],
            "CELERY_TIMEZONE": "UTC",
            "CELERY_UTC": "True",
            "CELERYD_NODES": "worker1 worker2 worker3 worker4",
            "CELERY_BIN": "/Library/Frameworks/Python.framework/Versions/3.8/bin/celery",
            "CELERY_APP": "dproxy.runner.runner:app",
            "CELERYD_CHDIR": "/opt/deployment/",
            "CELERYD_OPTS": "--time - limit = 300 - -concurrency = 8",
            "CELERYD_LOG_LEVEL": "INFO",
            "CELERYD_LOG_FILE": "/var/log/celery/%n%I.log",
            "CELERYD_PID_FILE": "/var/run/celery/%n.pid",
            "CELERYD_USER": "deployment",
            "CELERYD_GROUP": "deployment",
            "CELERY_CREATE_DIRS": 1
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
    ENV_FILE = ENV_FILE
    RETRY = get_env("RETRY")
    TOKEN = get_env("TOKEN")

    CELERY_BROKER_URL = get_env("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = get_env("CELERY_RESULT_BACKEND")
    CELERY_TASK_SERIALIZER = get_env("CELERY_TASK_SERIALIZER")
    CELERY_RESULT_SERIALIZER = get_env("CELERY_RESULT_SERIALIZER")
    CELERY_ACCEPT_CONTENT = get_env("CELERY_ACCEPT_CONTENT")
    CELERY_TIMEZONE = get_env("CELERY_TIMEZONE")
    CELERY_UTC = get_env("CELERY_UTC")

    CELERYD_NODES = get_env("CELERYD_NODES")
    CELERY_BIN = get_env("CELERY_BIN")
    CELERY_APP = get_env("CELERY_APP")
    CELERYD_CHDIR = get_env("CELERYD_CHDIR")
    CELERYD_OPTS = get_env("CELERYD_OPTS")
    CELERYD_LOG_LEVEL = get_env("CELERYD_LOG_LEVEL")
    CELERYD_LOG_FILE = get_env("CELERYD_LOG_FILE")
    CELERYD_PID_FILE = get_env("CELERYD_PID_FILE")
    CELERYD_USER = get_env("CELERYD_USER")
    CELERYD_GROUP = get_env("CELERYD_GROUP")
    CELERY_CREATE_DIRS = get_env("CELERY_CREATE_DIRS")


def get_logger():
    logger = logging.getLogger("dproxy")
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
