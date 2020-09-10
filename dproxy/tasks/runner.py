from celery import Celery
from celery.signals import after_setup_task_logger
from celery.app.log import TaskFormatter

from dproxy.config.config import Config
c = Config


def make_runner(app):
    runner = Celery(
        "dproxy",
        broker=c.CELERY_BROKER_URL,
        backend=c.CELERY_RESULT_BACKEND,
        task_serializer=c.CELERY_TASK_SERIALIZER,
        result_serializer=c.CELERY_RESULT_SERIALIZER,
        accept_content=c.CELERY_ACCEPT_CONTENT,
        timezone=c.CELERY_TIMEZONE,
        enable_utc=c.CELERY_UTC,
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
    runner.autodiscover_tasks(["tasks.deployment", "tasks.update"])

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
