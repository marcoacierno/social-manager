import tweepy
from constance import config
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from .provider import Provider


class TwitterProvider(Provider):
    NAMESPACE = "twitter"

    @property
    def urls(self):
        return [
            {
                "path": "authenticate/",
                "callback": self.authenticate,
                "name": "authenticate",
            },
            {"path": "callback/", "callback": self.callback, "name": "callback"},
        ]

    def authenticate(self, request):
        auth = tweepy.OAuthHandler(
            self.settings["CONSUMER_TOKEN"],
            self.settings["CONSUMER_SECRET"],
            request.build_absolute_uri(reverse("twitter:callback")),
        )

        try:
            redirect_url = auth.get_authorization_url()
            request.session["twitter_request_token"] = auth.request_token

            return redirect(redirect_url)
        except tweepy.TweepError as e:
            print("unable to fetch authorization url", e)
            messages.error(request, "Unable to link Twitter")
            return redirect(reverse("admin:index"))

    def callback(self, request):
        request_token = request.session.get("twitter_request_token")
        request.session.delete("twitter_request_token")

        oauth_verified = request.GET.get("oauth_verifier")

        auth = self._auth
        auth.request_token = request_token

        try:
            auth.get_access_token(oauth_verified)
        except tweepy.TweepError as e:
            print("unable to get access token", e)
            messages.error(
                request, f"Unable to get Twitter access token: {e.reason} {e.api_code}"
            )
            return redirect(reverse("admin:index"))

        config.TWITTER_ACCESS_TOKEN = auth.access_token
        config.TWITTER_ACCESS_TOKEN_SECRET = auth.access_token_secret

        messages.success(request, "Twitter linked!")
        return redirect(reverse("admin:index"))

    def publish_post(self, post):
        super().publish_post(post)

        from posts.models import Metadata

        api = self._api
        status = api.update_status(post.content)

        Metadata.objects.create(
            post=post,
            remote_id=status.id,
            provider_name=self.NAMESPACE,
            payload=status._json,
        )

        return status

    def delete_post(self, id):
        api = self._api
        api.destroy_status(id)

    @property
    def active_page(self):
        return {
            "id": None,
            "access_token": config.TWITTER_ACCESS_TOKEN,
            "access_token_secret": config.TWITTER_ACCESS_TOKEN_SECRET,
        }

    @property
    def pages(self):
        return []

    @property
    def _auth(self):
        return tweepy.OAuthHandler(
            self.settings["CONSUMER_TOKEN"], self.settings["CONSUMER_SECRET"]
        )

    @property
    def _api(self):
        auth = self._auth

        if config.TWITTER_ACCESS_TOKEN:
            auth.set_access_token(
                config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET
            )

        return tweepy.API(auth)

    @property
    def is_active(self):
        return bool(config.TWITTER_ACCESS_TOKEN)
