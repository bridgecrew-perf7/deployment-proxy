import os
from dotenv import load_dotenv
load_dotenv("/etc/default/dproxy")


class Config:
    HOSTNAME = os.getenv("HOSTNAME")
    IP = os.getenv("IP")
    STATE = os.getenv("STATE")
    GROUP = os.getenv("GROUP")
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    LOCATION = os.getenv("LOCATION")
    TOKEN = os.getenv("TOKEN")
    DEPLOYMENT_API_URI = os.getenv("DEPLOYMENT_API_URI")
