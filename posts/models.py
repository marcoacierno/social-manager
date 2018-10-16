from django.db import models
from django.utils import timezone
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from providers import get_all_providers


class Post(TimeStampedModel, StatusModel):
    STATUS = Choices("draft", "scheduled", "published")

    title = models.CharField(max_length=80)
    content = models.TextField()

    published_at = models.DateTimeField(blank=True, null=True)
    scheduled_at = models.DateTimeField(blank=True, null=True)

    def publish(self):
        if self.status == self.STATUS.published:
            return False

        self.status = self.STATUS.published
        self.published_at = timezone.now()

        for provider in get_all_providers():
            provider.publish_post(self)

        return True

    def __str__(self):
        return f"{self.title} - {self.status}"


class Metadata(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    provider_name = models.CharField(max_length=50)
    remote_id = models.TextField()
