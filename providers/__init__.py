from typing import Dict, List

from .facebook import FacebookProvider
from .provider import Provider
from .twitter import TwitterProvider

__all__ = ["FacebookProvider", "TwitterProvider"]

PROVIDERS: Dict[str, Provider] = {}
PROVIDERS[FacebookProvider.NAMESPACE] = FacebookProvider
PROVIDERS[TwitterProvider.NAMESPACE] = TwitterProvider

PROVIDERS_INSTANCES = {}


def get_provider(namespace: str) -> Provider:
    if namespace not in PROVIDERS:
        raise ValueError(f"Invalid provider {namespace}")

    if namespace not in PROVIDERS_INSTANCES:
        PROVIDERS_INSTANCES[namespace] = PROVIDERS[namespace]()

    return PROVIDERS_INSTANCES[namespace]


def get_all_providers() -> List[Provider]:
    return [get_provider(provider) for provider in PROVIDERS]
