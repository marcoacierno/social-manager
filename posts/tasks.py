from django.utils import timezone

from providers import get_all_providers, get_provider
from providers.exceptions import SocialProviderException
from social_manager.celery import app


@app.task
def publish_post(post_id):
    from .models import Post

    post = Post.objects.get(id=post_id)

    if not post.can_publish:
        print("cannot publish")
        return

    for provider in get_all_providers():
        try:
            provider.publish_post(post)
        except SocialProviderException as e:
            print("Unable to post: ", e)

    post.published_at = timezone.now()
    post.status = Post.STATUS.published
    post.save()


@app.task
def delete_post_on_social(metadata_id):
    from .models import Metadata

    try:
        metadata = Metadata.objects.get(id=metadata_id)
    except Metadata.DoesNotExist:
        print(f"Metadata ID {metadata_id} does not exist")
        return

    if metadata.status != Metadata.STATUS.deleting:
        print(
            f"Metadata status is not {Metadata.STATUS.deleting}, maybe the `delete` was reverted?"
        )
        return

    provider = get_provider(metadata.provider_name)
    provider.delete_post(metadata.remote_id)

    metadata.status = Metadata.STATUS.deleted
    metadata.save()
