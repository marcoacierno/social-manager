from django.db import models
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from .tasks import publish_post


class Post(TimeStampedModel, StatusModel):
    STATUS = Choices("draft", "scheduled", "publishing", "published")

    title = models.CharField(max_length=80)
    content = models.TextField()

    published_at = models.DateTimeField(blank=True, null=True)
    scheduled_at = models.DateTimeField(blank=True, null=True)

    @property
    def can_publish(self):
        return self.status in (
            self.STATUS.draft,
            self.STATUS.scheduled,
            self.STATUS.publishing,
        )

    def publish(self):
        if not self.can_publish:
            return False

        self.status = self.STATUS.publishing
        publish_post.delay(self.id)
        return True

    def __str__(self):
        return f"{self.title} - {self.status}"


class Metadata(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    provider_name = models.CharField(max_length=50)
    remote_id = models.TextField()
