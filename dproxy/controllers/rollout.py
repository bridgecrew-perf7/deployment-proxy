import os
import requests
from flask import request

from dproxy.config import Config


def post_rollout():
    data = request.get_json()

    # Post state updating
    headers = {"Authorization": Config.TOKEN}
    payload = {"hostname": data["hostname"], "state": "updating"}
    r = requests.patch("https://deployment.unifiedlayer.com/api/1.0.0/server", headers=headers, json=payload,
                       verify=False)

    try:
        for pkg in data["versionlock"]:
            os.system("yum versionlock add "+pkg)
        install_pkgs(data["versionlock"])
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        if "buildall" in data:
            os.system("/var/hp/common/bin/buildall -s")
        os.system("/bin/systemctl restart httpd")
        stat = os.system("/bin/systemctl status httpd.service")
        if stat != 0:
            raise Exception(stat)
        
        # Post server_history (action, yum_transaction_id, yum_rollback_id)
        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "Success",
                   "output": "deployment was successful", "yum_transaction_id": yum_transaction_id,
                   "yum_rollback_id": yum_rollback_id}
        r = requests.post("https://deployment.unifiedlayer.com/api/1.0.0/server/history/{}".format(data["hostname"]),
                          headers=headers, json=payload, verify=False)

        payload = {"hostname": data["hostname"], "state": "active"}
        r = requests.patch("https://deployment.unifiedlayer.com/api/1.0.0/server", headers=headers, json=payload,
                           verify=False)
        
        response = {
            "status": "success",
            "message": "Rollout successfully executed.",
        }
        return response, 201
    except Exception as e:
        # Post state error
        # Post server_history update failed
        payload = {"hostname": data["hostname"], "state": "error"}
        r = requests.patch("https://deployment.unifiedlayer.com/api/1.0.0/server", headers=headers, json=payload,
                           verify=False)
        
        yum_transaction_id = get_yum_transaction_id()
        yum_rollback_id = yum_transaction_id - 1
        payload = {"deployment_id": int(data["deployment_id"]), "action": "Update", "state": "Failed",
                   "yum_transaction_id": yum_transaction_id, "yum_rollback_id": yum_rollback_id}
        r = requests.post("https://deployment.unifiedlayer.com/api/1.0.0/server/history/{}".format(data["hostname"]),
                          headers=headers, json=payload, verify=False)
        
        response = {
            "status": "failed",
            "message": "POST rollout failed.",
            "exception": str(e)
        }
        return response, 409
