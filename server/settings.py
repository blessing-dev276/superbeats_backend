"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from environ import Env
from pathlib import Path
from datetime import timedelta

env = Env()
Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    str,
    "django-insecure-xcz0)!a!kskd-rjmf_99imsv+((sm)*et75jbzh*q4d0)=o@(h",
)

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = env("DEBUG", bool, False)

ALLOWED_HOSTS = ["*", env("DOMAIN_NAME", str, "http://localhost:8000")]

CSRF_TRUSTED_ORIGINS = [env("DOMAIN_NAME", str, "http://localhost:8000")]

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party libraries
    "rest_framework_simplejwt",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "drf_stripe",
    "drf_yasg",
    "storages",
    # my custom apps
    "account.apps.AccountConfig",
    "custom.apps.CustomConfig",
    'recipe.apps.RecipeConfig',
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

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "server/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "server/db.sqlite3",
    }
    if DEBUG
    else {
        "NAME": env("DBNAME", str, ""),
        "PORT": env("DBPORT", str, ""),
        "USER": env("DBUSER", str, ""),
        "HOST": env("DBHOST", str, ""),
        "PASSWORD": env("DBPASSWORD", str, ""),
        "ENGINE": "django.db.backends.postgresql",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

MEDIA_URL = "media/"

STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "media"

STATIC_ROOT = BASE_DIR / "static"

# STATICFILES_DIRS = [BASE_DIR / "statics"]

# STATICFILES_STORAGE = (
#     "django.contrib.staticfiles.storage.StaticFilesStorage"
#     if DEBUG
#     else "storages.backends.s3boto3.S3Boto3Storage"
# )

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# session

SESSION_COOKIE_AGE = 3600

SESSION_SAVE_EVERY_REQUEST = True

# cors configuration

CORS_ALLOW_ALL_ORIGINS = True

# email configuration

EMAIL_USE_TLS = True

EMAIL_PORT = ('EMAIL_PORT',int, 587)

EMAIL_HOST = env("EMAIL_HOST", str, "localhost")

EMAIL_HOST_USER = env("EMAIL_HOST_USER", str, "")

DEFAULT_FROM_EMAIL = env("EMAIL_HOST_USER", str, "")

EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", str, "")

# custom configuration

MAX_OTP_ROUND = env("MAX_OTP_ROUND", int, 3)

OTP_EXPIRE_MINUTE_TIME = env("OTP_EXPIRE_MINUTE_TIME", int, 5)

# aws storage configurations

AWS_LOCATION = "static"

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", str, "")

AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", str, "")

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", str, "")


# facebook

SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]

SOCIAL_AUTH_FACEBOOK_KEY = env("SOCIAL_AUTH_FACEBOOK_KEY", str, "")

SOCIAL_AUTH_FACEBOOK_SECRET = env("SOCIAL_AUTH_FACEBOOK_SECRET", str, "")

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {"fields": "id, name, email"}

# google

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ["email", "profile"]

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ["example.com"]

SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {"access_type": "offline"}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", str, "")

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", str, "")


AUTHENTICATION_BACKENDS = [
    # "social_core.backends.facebook.FacebookAppOAuth2",
    # # ...
    # "social_core.backends.facebook.FacebookOAuth2",
    # # ...
    # "social_core.backends.google.GoogleOAuth2",
    # ...
    "server.backends.CustomAuthBackend",
    # ...
]

# drf stripe configuration

DRF_STRIPE = {
    # ...
    "DJANGO_USER_EMAIL_FIELD": "email",
    # ...
    "STRIPE_API_SECRET": env("STRIPE_PRIVATE_KEY", str, ""),
    # ...
    "USER_CREATE_DEFAULTS_ATTRIBUTE_MAP": {"username": "email"},
    # ...
    "STRIPE_WEBHOOK_SECRET": env("STRIPE_WEBHOOK_SECRET", str, ""),
    # ...
}

SIMPLE_JWT = {
    # ...
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=5),
    # ...
    "TOKEN_OBTAIN_SERIALIZER": "server.serializers.TokenSerializer",
    # ...
}

REST_FRAMEWORK = {
    #  ...
    "DEFAULT_FILTER_BACKENDS": [
        "server.filters.DynamicSearchFilters",
        "rest_framework.filters.OrderingFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    #  ...
    "PAGE_SIZE": 20,
    #  ...
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    #  ...
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    #  ...
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    #  ...
}

# jazzmin configuration

JAZZMIN_SETTINGS = {
    # ...
    "show_sidebar": False,
    # ...
    "show_ui_builder": True,
    # ...
    "site_brand": "Superb Eats",
    # ...
    "site_title": "Superb Eats",
    # ...
    "site_header": "Superb Eats",
    # ...
    "related_modal_active": False,
    # ...
    "user_avatar": "profile.avatar",
    # ...
    "changeform_format": "carousel",
    # ...
    "welcome sign": "Welcom to Superb Eats",
    # ...
    # "welcome topmenu_links": [
    #     {"api": i} for i in ["auth", "account", "custom", "recipee"]
    # ],
    # ...
}
