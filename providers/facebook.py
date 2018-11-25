import logging
from datetime import datetime, timedelta

import facebook
from constance import config
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from .provider import Provider

logger = logging.getLogger("social_manager.providers.facebook")


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
            {
                "path": "deauthenticate/",
                "callback": self.deauthenticate,
                "name": "deauthenticate",
            },
            {"path": "redirect/", "callback": self.redirect, "name": "redirect"},
        ]

    @property
    def active_page(self):
        if not config.FACEBOOK_ACTIVE_PAGE_ID:
            return None

        return {
            "id": config.FACEBOOK_ACTIVE_PAGE_ID,
            "access_token": config.FACEBOOK_ACTIVE_PAGE_ACCESS_TOKEN,
        }

    def publish_post(self, post):
        super().publish_post(post)

        from posts.models import Metadata

        graph = get_graph_client(True)
        result = graph.put_object(
            config.FACEBOOK_ACTIVE_PAGE_ID, "feed", message=post.content
        )

        Metadata.objects.create(
            post=post,
            remote_id=result["id"],
            provider_name=self.NAMESPACE,
            payload=result,
        )
        return result

    def delete_post(self, id):
        graph = get_graph_client(True)

        try:
            graph.delete_object(id)
        except facebook.GraphAPIError as e:
            if e.code == 100:
                logger.exception(
                    "Unable to delete facebook post, maybe it's already removed?"
                )
                return

            raise

    def set_active_page(self, **kwargs):
        id = kwargs["page_id"][0]
        access_token = kwargs["page_access_token"][0]

        config.FACEBOOK_ACTIVE_PAGE_ID = id
        config.FACEBOOK_ACTIVE_PAGE_ACCESS_TOKEN = access_token
        return True

    def authenticate(self, request):
        graph = get_graph_client()
        fb_login_url = graph.get_auth_url(
            self.settings["APP_ID"],
            self._redirect_uri(request),
            self.settings["PERMISSIONS"],
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
            self.settings["APP_ID"],
            self.settings["APP_SECRET"],
        )

        config.FACEBOOK_ACCESS_TOKEN = access_token_data["access_token"]

        if "expires_in" in access_token_data:
            config.FACEBOOK_ACCESS_TOKEN_EXPIRES_AT = datetime.now() + timedelta(
                seconds=access_token_data["expires_in"]
            )

        messages.success(request, "Facebook access token set correctly!")
        return redirect(reverse("admin:index"))

    @property
    def is_active(self):
        return config.FACEBOOK_ACTIVE_PAGE_ID != -1

    def deauthenticate(self, request, **kwargs):
        super().deauthenticate()
        graph = get_graph_client(False)

        success = False
        try:
            success = graph.request("/me/permissions", method="DELETE")
            success = success["success"]
        except facebook.GraphAPIError as e:
            if (
                e.code == 190
                and "Error validating access token: The user has not authorized application"
                in e.message
            ):
                # if the user already has deauthorizated the app via facebook panel for example
                # we simply ignore the error and reset the saved values
                success = True
            else:
                raise

        if success:
            config.FACEBOOK_ACCESS_TOKEN = ""
            config.FACEBOOK_ACTIVE_PAGE_ID = -1
            config.FACEBOOK_ACTIVE_PAGE_ACCESS_TOKEN = ""
            messages.success(request, "Facebook settings resetted correctly!")
            return redirect(reverse("admin:index"))

        messages.error(request, "Unable to unlink your facebook account")
        return redirect(reverse("admin:index"))

    def _redirect_uri(self, request):
        return request.build_absolute_uri(reverse("facebook:redirect"))


def get_graph_client(page_token=False):
    access_token = (
        config.FACEBOOK_ACCESS_TOKEN
        if not page_token
        else config.FACEBOOK_ACTIVE_PAGE_ACCESS_TOKEN
    )
    graph = facebook.GraphAPI(access_token=access_token, version="3.0")
    return graph
