import os
import socket
from dotenv import load_dotenv
from collections import OrderedDict


class LastUpdated(OrderedDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
        

environment_file = "/etc/default/dproxy"
if os.getenv("ENV_FILE"):
    environment_file = os.getenv("ENV_FILE")
try:
    load_dotenv(environment_file)
except Exception as e:
    raise Exception(f"Unable to load environment {environment_file}: {e}")

config_file = "/etc/deployment/dproxy.conf"
if os.getenv("CONFIG_FILE"):
    config_file = os.getenv("CONFIG_FILE")
config = LastUpdated()
try:
    with open(config_file) as cfg:
        for line in cfg:
            try:
                (k, v) = line.split("=", 1)
                config[k] = v
            except:
                pass
except Exception as e:
    raise Exception(f"Unable to load configuration {config_file}: {e}")
    

def get_var(var):
    if os.getenv(var):
        return os.getenv(var)
    else:
        if var in config:
            return config[var]
        else:
            return None


class Config(object):
    HOSTNAME = get_var("HOSTNAME")
    IP = get_var("IP")
    LOCATION = get_var("LOCATION")
    ENVIRONMENT = get_var("ENVIRONMENT")
    DEPLOYMENT_PROXY_URI = get_var("DEPLOYMENT_PROXY_URI")
    DEPLOYMENT_API_URI = get_var("DEPLOYMENT_API_URI")
    ENV_FILE = get_var("ENV_FILE")

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