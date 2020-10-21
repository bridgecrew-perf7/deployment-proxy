import os
import socket
import configparser
from dotenv import load_dotenv


def load_config():
    try:
        config = configparser.ConfigParser()
        config.read("/etc/deployment/dproxy.ini")
        load_dotenv(config["proxy"]["ENVIRONMENT_FILE"])
        return config
    except Exception as e:
        raise Exception(f"configuration is missing or not accessible: {e}")
