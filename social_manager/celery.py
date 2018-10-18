import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_manager.settings.prod")

app = Celery("social_manager", broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from .crontab import publish_scheduled_posts

    sender.add_periodic_task(
        60.0, publish_scheduled_posts.s(), name="Post scheduled posts"
    )


if __name__ == "__main__":
    app.start()
