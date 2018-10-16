from abc import ABC, abstractmethod

from django.conf import settings


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

    @abstractmethod
    def publish_post(self, post):
        pass

    def set_active_page(self, **kwargs):
        raise NotImplemented()

    @property
    def settings(self):
        return settings.PROVIDERS[self.NAMESPACE.upper()]
