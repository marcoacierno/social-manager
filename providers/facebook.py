from datetime import datetime, timedelta

import facebook
from constance import config
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from .provider import Provider


class FacebookProvider(Provider):
    NAMESPACE = "facebook"

    @property
    def pages(self):
        graph = get_graph_client()
        pages = graph.get_connections(id="me", connection_name="accounts")

        return [
            {
                "name": page["name"],
                "access_token": page["access_token"],
                "id": page["id"],
            }
            for page in pages["data"]
        ]

    @property
    def urls(self):
        return [
            {
                "path": "authenticate/",
                "callback": self.authenticate,
                "name": "authenticate",
            },
            {"path": "redirect/", "callback": self.redirect, "name": "redirect"},
        ]

    @property
    def active_page(self):
        return {
            "id": config.FACEBOOK_ACTIVE_PAGE_ID,
            "access_token": config.FACEBOOK_ACTIVE_PAGE_ACCESS_TOKEN,
        }

    def set_active_page(self, **kwargs):
        id = kwargs["page_id"][0]
        access_token = kwargs["page_access_token"][0]

        config.FACEBOOK_ACTIVE_PAGE_ID = id
        config.FACEBOOK_ACTIVE_PAGE_ACCESS_TOKEN = access_token
        return True

    def authenticate(self, request):
        graph = get_graph_client()
        fb_login_url = graph.get_auth_url(
            settings.PROVIDERS["FACEBOOK"]["APP_ID"],
            self._redirect_uri(request),
            settings.PROVIDERS["FACEBOOK"]["PERMISSIONS"],
        )

        return redirect(fb_login_url)

    def redirect(self, request):
        code = request.GET.get("code", "")

        if not code:
            messages.error(request, "Unable to get the code from facebook")
            return redirect(reverse("admin:index"))

        graph = get_graph_client()
        access_token_data = graph.get_access_token_from_code(
            code,
            self._redirect_uri(request),
            settings.PROVIDERS["FACEBOOK"]["APP_ID"],
            settings.PROVIDERS["FACEBOOK"]["APP_SECRET"],
        )

        config.FACEBOOK_ACCESS_TOKEN = access_token_data["access_token"]
        config.FACEBOOK_ACCESS_TOKEN_EXPIRES_AT = datetime.now() + timedelta(
            seconds=access_token_data["expires_in"]
        )

        messages.success(request, "Facebook access token set correctly!")
        return redirect(reverse("admin:index"))

    def _redirect_uri(self, request):
        return request.build_absolute_uri(reverse("facebook:redirect"))


def get_graph_client():
    graph = facebook.GraphAPI(access_token=config.FACEBOOK_ACCESS_TOKEN, version="3.0")
    return graph
