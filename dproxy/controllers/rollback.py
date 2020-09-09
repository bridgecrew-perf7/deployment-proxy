import os
import requests
from flask import request

from dproxy.config import Config


def post_rollback():
    data = request.get_json()
    headers = {"Authorization": Config.TOKEN}
    payload = {"hostname": data["hostname"], "state": "updating"}
    r = requests.patch("https://deployment.unifiedlayer.com/api/1.0.0/server", headers=headers, json=payload,
                       verify=False)
    
    try:
        os.system("yum -y history rollback {}".format(data["yum_rollback_id"]))
        for pkg in data["versionlock"]:
            os.system("yum versionlock add "+pkg)
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        if "buildall" in data:
            os.system("/var/hp/common/bin/buildall -s")
        os.system("/bin/systemctl restart httpd")
        stat = os.system("/bin/systemctl status httpd.service")
        if stat != 0:
            raise Exception(stat)

        payload = {"deployment_id": data["deployment_id"], "action": "Update", "state": "Success",
                   "yum_transaction_id": yum_transaction_id, "yum_rollback_id": yum_rollback_id}
        r = requests.post("https://deployment.unifiedlayer.com/api/1.0.0/server/history/{}".format(data["hostname"]),
                          headers=headers, json=payload, verify=False)

        payload = {"hostname": data["hostname"], "state": "Active"}
        r = requests.patch("https://deployment.unifiedlayer.com/api/1.0.0/server", headers=headers, json=payload,
                           verify=False)

        response = {
            "status": "success",
            "message": "Rollback successfully executed.",
        },
        return response, 201
        "status": "success",
                "message": "Deployment successfully rolled back.",
        }
        return response, 201
    except Exception as e:
        payload = {"hostname": data["hostname"], "state": "error"}
        r = requests.patch("https://deployment.unifiedlayer.com/api/1.0.0/server", headers=headers, json=payload,
                           verify=False)
        
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        
        payload = {"deployment_id": data["deployment_id"], "action": "Update", "state": "Failed",
                   "yum_transaction_id": yum_transaction_id, "yum_rollback_id": yum_rollback_id}
        r = requests.post("https://deployment.unifiedlayer.com/api/1.0.0/server/history/{}".format(data["hostname"]),
                          headers=headers, json=payload, verify=False)
        
        response = {
            "status": "fail",
            "message": "Deployment rollback failed.",
            "exception": str(e)
        }
        return response, 409

