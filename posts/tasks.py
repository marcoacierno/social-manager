from django.utils import timezone

from providers import get_all_providers
from social_manager.celery import app


@app.task
def publish_post(post_id):
    from .models import Post

    post = Post.objects.get(id=post_id)

    if not post.can_publish:
        print("cannot publish")
        return

    for provider in get_all_providers():
        provider.publish_post(post)

    post.published_at = timezone.now()
    post.status = Post.STATUS.published
    post.save()
