import logging

from celery import Task


logger = logging.getLogger("social_manager.tasks.exceptions")


class ErrorHandler(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.exception(f"Failed whle running task id {task_id}", exc_info=exc)
        super().on_failure(exc, task_id, args, kwargs, einfo)
