from dproxy.tasks.deployment.tasks import rollout, rollback, complete
from dproxy.tasks.update.tasks import server_update

from threading import Thread
from celery import chord
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class Watcher(object):
    def __init__(self, task, inventory):
        self.task = task
        self.inventory = inventory
        thread = Thread(target=self.run(inventory), args=())
        thread.daemon = True
        thread.start()

    def run(self, inventory):
        if self.task == "rollout":
            chord(
                [rollout.s(data=host) for host in inventory["hosts"]],
                complete.s(deployment_id=1),
            ).delay()
        elif self.task == "rollback":
            chord(
                [rollback.s(data=host) for host in inventory["hosts"]],
                complete.s(deployment_id=1),
            ).delay()
        elif self.task == "server_update":
            chord(
                [server_update.s(data=host) for host in inventory["hosts"]],
                complete.s(deployment_id=1),
            ).delay()
