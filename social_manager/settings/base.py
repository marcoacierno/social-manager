import datetime

import environ

root = environ.Path(__file__) - 3

env = environ.Env(DEBUG=(bool, False), ALLOWED_HOSTS=(list, []), SECRET_KEY=(str))
env.read_env(root(".env"))

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "providers",
    "posts",
    "socialadmin.apps.SocialAdminConfig",
    "constance",
    "constance.backends.database",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "social_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [root("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "providers.context_processors.providers",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "social_manager.wsgi.application"

DATABASES = {"default": env.db()}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

PROVIDERS = {
    "FACEBOOK": {
        "APP_ID": env("FACEBOOK_APP_ID"),
        "APP_SECRET": env("FACEBOOK_APP_SECRET"),
        "PERMISSIONS": ["manage_pages", "publish_pages"],
    }
}

CONSTANCE_CONFIG = {
    "FACEBOOK_ACCESS_TOKEN": ("", "Facebook access token"),
    "FACEBOOK_ACCESS_TOKEN_EXPIRES_AT": (datetime.datetime(1990, 1, 1), "Expiry date"),
    "FACEBOOK_ACTIVE_PAGE_ID": (-1, "Active Facebook page"),
    "FACEBOOK_ACTIVE_PAGE_ACCESS_TOKEN": ("", "Active Facebook page access token"),
}

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
