import os
import socket
from dotenv import load_dotenv
from collections import OrderedDict


class LastUpdated(OrderedDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


if os.getenv("ENV_FILE"):
    load_dotenv(os.getenv("ENV_FILE"))
elif os.path.exists(".env"):
    load_dotenv(".env")
elif os.path.exists("/etc/default/dproxy"):
    load_dotenv("/etc/default/dproxy")
else:
    raise Exception("No Environment File Found!")


def get_config():
    if os.getenv("CONFIG_FILE"):
        config_file = os.getenv("CONFIG_FILE")
    else:
        config_file = "/etc/deployment/dproxy.conf"

    if os.path.exists(config_file):
        config = LastUpdated()
        with open(config_file) as cfg:
            for line in cfg:
                try:
                    (k, v) = line.split("=", 1)
                    config[k] = v
                except:
                    pass
        return config
    else:
        return None


def get_var(var):
    config = get_config()
    if os.getenv(var):
        return os.getenv(var)
    else:
        if config:
            if var in config:
                return config[var]
            else:
                return None
        else:
            return None


class Config(object):
    SECRET_KEY = get_var("SECRET_KEY")
    STATE = get_var("STATE")
    HOSTNAME = get_var("HOSTNAME")
    IP = get_var("IP")
    PORT = get_var("PORT")
    API_VERSION = get_var("API_VERSION")
    LOCATION = get_var("LOCATION")
    ENVIRONMENT = get_var("ENVIRONMENT")
    API_HOSTNAME = get_var("API_HOSTNAME")
    API_PORT = get_var("API_PORT")
    DEPLOYMENT_PROXY_URI = "http://" + HOSTNAME + ":" + PORT + "/api/" + API_VERSION
    DEPLOYMENT_API_URI = (
        "http://" + API_HOSTNAME + ":" + API_PORT + "/api/" + API_VERSION
    )
    ENV_FILE = get_var("ENV_FILE")
    LOG_FILE = get_var("LOG_FILE")
    LOG_MAX_BYTES = get_var("LOG_MAX_BYTES")
    LOG_BACKUP_COUNT = get_var("LOG_BACKUP_COUNT")

    SECRET_KEY = get_var("SECRET_KEY")
    TOKEN = get_var("TOKEN")

    CELERY_BROKER_URL = get_var("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = get_var("CELERY_RESULT_BACKEND")
    CELERY_TASK_SERIALIZER = get_var("CELERY_TASK_SERIALIZER")
    CELERY_RESULT_SERIALIZER = get_var("CELERY_RESULT_SERIALIZER")
    CELERY_ACCEPT_CONTENT = get_var("CELERY_ACCEPT_CONTENT")
    CELERY_TIMEZONE = get_var("CELERY_TIMEZONE")
    CELERY_UTC = get_var("CELERY_UTC")
    CELERYD_NODES = get_var("CELERYD_NODES")
    CELERY_BIN = get_var("CELERY_BIN")
    CELERY_APP = get_var("CELERY_APP")
    CELERYD_CHDIR = get_var("CELERYD_CHDIR")
    CELERYD_OPTS = get_var("CELERYD_OPTS")
    CELERYD_LOG_LEVEL = get_var("CELERYD_LOG_LEVEL")
    CELERYD_LOG_FILE = get_var("CELERYD_LOG_FILE")
    CELERYD_PID_FILE = get_var("CELERYD_PID_FILE")
    CELERYD_USER = get_var("CELERYD_USER")
    CELERYD_GROUP = get_var("CELERYD_GROUP")
    CELERY_CREATE_DIRS = get_var("CELERY_CREATE_DIRS")

    RETRY = get_var("RETRY")
    BACKOFF_FACTOR = get_var("BACKOFF_FACTOR")
    STATUS_FORCELIST = get_var("STATUS_FORCELIST")
    METHOD_WHITELIST = get_var("METHOD_WHITELIST")
    DEFAULT_TIMEOUT = get_var("DEFAULT_TIMEOUT")
