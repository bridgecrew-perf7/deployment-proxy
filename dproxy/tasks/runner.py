from dproxy.config import Config

from celery import Celery
from celery.signals import after_setup_task_logger
from celery.app.log import TaskFormatter


def make_runner(app):
    runner = Celery(
        "dproxy",
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND,
        task_serializer=Config.CELERY_TASK_SERIALIZER,
        result_serializer=Config.CELERY_RESULT_SERIALIZER,
        accept_content=Config.CELERY_ACCEPT_CONTENT,
        timezone=Config.CELERY_TIMEZONE,
        enable_utc=Config.CELERY_UTC,
        task_default_queue="dproxy",
        database_table_schemas={
            'task': 'celery',
            'group': 'celery',
        },
        database_table_names={
            'task': 'dproxy_taskmeta',
            'group': 'dproxy_groupmeta',
        }
    )

    runner.conf.update(result_expires=3600)
    runner.autodiscover_tasks(["dproxy.tasks.deployment", "dproxy.tasks.update", "dproxy.tasks.server"])

    class ContextTask(runner.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    runner.Task = ContextTask
    return runner


@after_setup_task_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    for handler in logger.handlers:
        handler.setFormatter(TaskFormatter("%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s"))
