from dproxy.util.config import Config
from dproxy.util.logger import get_logger
from dproxy.util.http_helper import get_http

import os
import sys
from collections import OrderedDict
from subprocess import check_output, check_call, Popen

logger = get_logger()


class LastUpdated(OrderedDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


def update_env(key, value):
    """
    Set a key value pair in the environment file and export to the os
    :param: key string
    :param: value string
    :return: True or False
    """
    try:
        os.environ[key] = value
        env = LastUpdated()
        with open(Config.ENV_FILE) as f:
            for line in f:
                try:
                    (k, v) = line.split("=", 1)
                    env[k] = v
                except:
                    pass
        env[key] = value

        with open(Config.ENV_FILE, "w") as f:
            for k in env.keys():
                line = f"{k}={env[k]}"
                if "\n" in line:
                    f.write(line)
                else:
                    f.write(line + "\n")
        return True
    except Exception as e:
        logger.error(f"Update Environment Failed: {e}")
        return False


def set_state(state):
    """
    Set the dproxy state in the environment and the deployment-api to the correct state.
    :param: state enum[NEW ACTIVE UPDATING ERROR DISABLED]
    :return: True or False
    """
    try:
        headers = {"Authorization": Config.TOKEN}
        data = {"state": state}
        http = get_http()
        r = http.patch(
            f"{Config.DEPLOYMENT_API_URI}/deployment/proxy/hostname/{Config.HOSTNAME}",
            headers=headers,
            json=data,
        )
        resp = r.json()
        logger.debug(f"Updated Proxy: {resp} {r.status_code}")
        update_env("STATE", state)
        os.environ["STATE"] = state
        return True
    except Exception as e:
        logger.error(f"SET STATE FAILED: {e}")
        return False


def register_proxy():
    """
    Register a new proxy
    retrieve and cache a token from deployment-api
    """
    try:
        data = {
            "hostname": Config.HOSTNAME,
            "ip": Config.IP,
            "state": "NEW",
            "location": Config.LOCATION,
            "environment": Config.ENVIRONMENT,
            "created_by": "dproxy",
        }
        http = get_http()
        r = http.post(f"{Config.DEPLOYMENT_API_URI}/register/proxy", json=data)
        resp = r.json()
        logger.info(resp)
        if "token" in resp:
            update_env("TOKEN", resp["token"])
            os.environ["TOKEN"] = resp["token"]
            set_state("ACTIVE")
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Register Proxy Failed: {e}")
        return False


def install_pkgs(packages):
    packages = [x.encode("utf-8") for x in packages]
    packages = " ".join(packages)
    check_call("sudo yum clean all", verbose=False)
    stat = check_call(f"sudo yum -y install {packages}", verbose=False)
    if stat != 0:
        raise Exception(stat)


def restart_service(service):
    restart = f"systemctl restart {service}"
    Popen([sys.executable, restart])
