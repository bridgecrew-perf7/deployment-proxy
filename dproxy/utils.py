from dproxy.config import Config

import os
import sys
import requests
from collections import OrderedDict
from requests.adapters import HTTPAdapter
from subprocess import check_output, check_call, Popen
from requests.packages.urllib3.util.retry import Retry


class LastUpdated(OrderedDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


def get_http():
    retry_strategy = Retry(
        total=Config.RETRY,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    return http


def install_pkgs(packages):
    packages = [x.encode('utf-8') for x in packages]
    packages = ' '.join(packages)
    check_call("sudo yum clean all", verbose=False)
    stat = check_call(f"sudo yum -y install {packages}", verbose=False)
    if stat != 0:
        raise Exception(stat)


def restart_service(service):
    restart = "systemctl restart " + service
    Popen([sys.executable, restart])


def update_env(key, value):
    os.environ[key] = value
    env = LastUpdated()
    with open(Config.ENV_FILE) as f:
        for line in f:
            (k, v) = line.split("=", 1)
            env[k] = v
    env[key] = value

    with open(Config.ENV_FILE, "w") as f:
        for k in env.keys():
            line = f"{k}={env[k]}"
            if "\n" in line:
                f.write(line)
            else:
                f.write(line+"\n")
