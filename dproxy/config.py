import os
from dotenv import load_dotenv
load_dotenv("/etc/default/dproxy")


class Config:
    DEPLOYMENT_API_URI = os.getenv("DEPLOYMENT_API_URI")
    TOKEN = os.getenv("TOKEN")
