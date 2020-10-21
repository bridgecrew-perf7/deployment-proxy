from dproxy.util.config import load_config
from dproxy.util.http_helper import get_http

import os
import sys
from subprocess import check_output, check_call, Popen

config = load_config()


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
        with open(config["environment_file"]) as f:
            for line in f:
                try:
                    (k, v) = line.split("=", 1)
                    env[k] = v
                except:
                    pass
        env[key] = value

        with open(config["environment_file"], "w") as f:
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
        headers = {"Authorization": config["token"]}
        data = {"hostname": config["hostname"], "state": state}
        http = get_http()
        r = http.patch(f"{config['deployment_api_uri']}/server", headers=headers, json=data)
        resp = r.json()
        logger.debug(f"Updated Proxy: {resp} {r.status_code}")
        update_env("STATE", "ACTIVE")
        os.environ["STATE"] = "ACTIVE"
        return True
    except Exception as e:
        logger.error(f"SET STATE FAILED: {e}")
        return False


def register_proxy():
    try:
        data = {
            "hostname": config["hostname"],
            "ip": config["ip"],
            "state": "NEW",
            "location": config["location"],
            "environment": config["environment"],
            "url": config["url"]
        }
        http = get_http()
        r = http.post(f"{config['deployment_api_uri']}/register/proxy", json=data))
        resp = r.json()
        update_env("TOKEN", resp["token"])
        os.environ["TOKEN"] = resp["token"]
        return True
    except Exception as e:
        logger.error(f"Register Proxy Failed: {e}")
        return False

        
def install_pkgs(packages):
    packages = [x.encode('utf-8') for x in packages]
    packages = ' '.join(packages)
    check_call("sudo yum clean all", verbose=False)
    stat = check_call(f"sudo yum -y install {packages}", verbose=False)
    if stat != 0:
        raise Exception(stat)


def restart_service(service):
    restart = f"systemctl restart {service}"
    Popen([sys.executable, restart])
