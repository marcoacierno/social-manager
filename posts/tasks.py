import logging

from django.utils import timezone

from providers import get_all_providers, get_provider
from providers.exceptions import SocialProviderException
from social_manager.celery import app

logger = logging.getLogger("social_manager.tasks.posts")


@app.task
def publish_post(post_id):
    from .models import Post

    post = Post.objects.get(id=post_id)

    if not post.can_publish:
        logger.warning(f"Cannot publish {post_id} because status is: {post.status}")
        return

    for provider in get_all_providers():
        try:
            provider.publish_post(post)
        except SocialProviderException as e:
            logger.exception(f"Unable to post {post_id}")

    post.published_at = timezone.now()
    post.status = Post.STATUS.published
    post.save()

    logger.info(f"Post {post_id} ({post.title}) published!")


@app.task
def delete_post_on_social(metadata_id):
    from .models import Metadata

    try:
        metadata = Metadata.objects.get(id=metadata_id)
    except Metadata.DoesNotExist:
        logger.error(f"Metadata ID {metadata_id} does not exist")
        return

    if metadata.status != Metadata.STATUS.deleting:
        logger.error(
            f"Metadata status is not {Metadata.STATUS.deleting}, maybe the `delete` was reverted?"
        )
        return

    provider = get_provider(metadata.provider_name)
    provider.delete_post(metadata.remote_id)

    metadata.status = Metadata.STATUS.deleted
    metadata.save()

    logger.info(
        f"Metadata {metadata_id} of post ID {metadata.post_id} deleted from {metadata.provider_name}"
    )
