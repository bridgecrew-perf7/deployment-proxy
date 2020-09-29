from dproxy.tasks.deployment.tasks import notify_complete

from celery import group
from threading import Thread
from celery.task import chord


class Watcher(object):
    def __init__(self, tasks):
        self.tasks = tasks
        thread = threading.Thread(target=self.run(tasks), args=())
        thread.daemon = True
        thread.start()

    def run(self, tasks):
        chord(tasks, notify_complete.s())()