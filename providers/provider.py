from abc import ABC, abstractmethod

from django.conf import settings

from .exceptions import SocialProviderException


class Provider(ABC):
    NAMESPACE = None

    @property
    @abstractmethod
    def pages(self):
        pass

    @property
    @abstractmethod
    def urls(self):
        pass

    @property
    @abstractmethod
    def active_page(self):
        pass

    @property
    @abstractmethod
    def is_active(self):
        pass

    @abstractmethod
    def publish_post(self, post):
        if not self.is_active:
            raise SocialProviderException(f"Provider {self.NAMESPACE} not active")

        from posts.models import Metadata

        if Metadata.objects.filter(
            post=post, provider_name=self.NAMESPACE, status=Metadata.STATUS.created
        ).exists():
            raise SocialProviderException(f"Post already exists on {self.NAMESPACE}")

    @abstractmethod
    def delete_post(self, id):
        if not self.is_active:
            raise SocialProviderException(f"Provider {self.NAMESPACE} not active")

    @abstractmethod
    def deauthenticate(self):
        if not self.is_active:
            raise SocialProviderException(
                f"Provider {self.NAMESPACE} not authenticated"
            )

    def set_active_page(self, **kwargs):
        raise NotImplemented()

    @property
    def settings(self):
        return settings.PROVIDERS[self.NAMESPACE.upper()]
