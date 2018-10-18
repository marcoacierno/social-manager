import logging

from django.utils import timezone

from .celery import app
from .error_handler import ErrorHandler

logger = logging.getLogger("social_manager.tasks.crontab")


@app.task(base=ErrorHandler)
def publish_scheduled_posts():
    from posts.models import Post

    now = timezone.now()

    logger.debug("Checking scheduled posts...")

    posts_to_publish = Post.objects.filter(
        scheduled_at__lte=now, status=Post.STATUS.scheduled
    )

    posts_count = 0

    for post in posts_to_publish:
        post.publish()
        posts_count += 1

    logger.debug(f"Found {posts_count} posts to publish...")
