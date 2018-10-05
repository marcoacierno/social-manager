from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path

from . import PROVIDERS, get_provider
from .views import provider_pages_index

urlpatterns = [
    path("admin/provider/<slug:slug>/", provider_pages_index, name="provider-index")
]

for provider in PROVIDERS:
    instance = get_provider(provider)

    provider_urls = ([], provider)

    for url in instance.urls:
        provider_urls[0].append(
            path(
                f'{url["path"]}',
                staff_member_required(url["callback"]),
                name=url["name"] if "name" in url else None,
            )
        )

    urlpatterns.append(path(f"{provider}/", include(provider_urls)))
