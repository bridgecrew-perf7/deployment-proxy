import os
import logging
from dotenv import load_dotenv

ENV_FILE = os.getenv("ENV_FILE")
if PROXY_ENV == "development":
    load_dotenv(ENV_FILE)
else:
    load_dotenv(ENV_FILE)


class Config(object):
    HOSTNAME = os.getenv("HOSTNAME")
    IP = os.getenv("IP")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    STATE = os.getenv("STATE")
    LOCATION = os.getenv("LOCATION")
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    TOKEN = os.getenv("TOKEN")
    DEPLOYMENT_PROXY_URI = os.getenv("DEPLOYMENT_PROXY_URI")
    DEPLOYMENT_API_URI = os.getenv("DEPLOYMENT_API_URI")
    ENV_FILE = os.getenv("ENV_FILE")
    
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
