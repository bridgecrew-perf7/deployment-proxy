from dproxy.tasks.deployment.tasks import rollout
from dproxy.tasks.watcher import Watcher

import os
from flask import request
from celery.task import task
from celery import signature


def post_rollout():
    data = request.get_json()
    try:
        tasks = []
        for host in data:
            tasks.append(rollout.s(host))
        Watcher(tasks)
        response = {
            "status": "success",
            "message": "Rollout successfully started",
        }
        return response, 202
    except Exception as e:
        response = {
            "status": "failure",
            "message": "Rollout failed to start",
            "exception": str(e)
        }
        return response, 409
