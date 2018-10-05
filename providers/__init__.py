from typing import Dict

from .facebook import FacebookProvider
from .provider import Provider

__all__ = ["FacebookProvider"]

PROVIDERS: Dict[str, Provider] = {}
PROVIDERS[FacebookProvider.NAMESPACE] = FacebookProvider

PROVIDERS_INSTANCES = {}


def get_provider(namespace: str) -> Provider:
    if namespace not in PROVIDERS:
        raise ValueError(f"Invalid provider {namespace}")

    if namespace not in PROVIDERS_INSTANCES:
        PROVIDERS_INSTANCES[namespace] = PROVIDERS[namespace]()

    return PROVIDERS_INSTANCES[namespace]
