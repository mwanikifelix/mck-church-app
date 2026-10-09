import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")  # backend/.env — matches docker-compose.yml's env_file path


def env_bool(name, default="0"):
    return os.environ.get(name, default) in ("1", "true", "True")


def env_list(name, default=""):
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-insecure-key-change-me")
DEBUG = env_bool("DEBUG", "0")
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "django_celery_beat",
    "drf_spectacular",

    # local apps — added one module at a time as each is built
    "apps.accounts",
    "apps.church",
    "apps.groups",
    "apps.hbc",
    "apps.pastoral",
    "apps.chatbot",
    "apps.scripture",
    "apps.about",
    "apps.registration",
    "apps.attendance",
    "apps.giving",
    "apps.content",
    "apps.prayer",
    "apps.events",
    "apps.notifications",
    "apps.membership",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --- Database — self-contained postgres service defined below,
# creates the mck_church database automatically on first start ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "mck_church"),
        "USER": os.environ.get("DB_USER", "admin"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "CHANGE_ME_DEV_DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST", "postgres"),   # matches the postgres service name below
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- DRF / JWT ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "USER_ID_FIELD": "id",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "MCK Church App API",
    "DESCRIPTION": "Accounts, Groups, Events, Giving, Pastoral, Content, Notifications",
    "VERSION": "0.1.0",
}

# --- CORS (Flutter app + Vue admin) ---
CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
)

# --- Redis — self-contained redis service defined below ---
# REDIS_DB picks a logical database index, in case you later point this
# at a shared instance — harmless default otherwise.
_REDIS_HOST = os.environ.get("REDIS_HOST", "redis")   # matches the redis service name below
_REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
_REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
_REDIS_DB = os.environ.get("REDIS_DB", "0")
_REDIS_URL = (
    f"redis://:{_REDIS_PASSWORD}@{_REDIS_HOST}:{_REDIS_PORT}/{_REDIS_DB}"
    if _REDIS_PASSWORD
    else f"redis://{_REDIS_HOST}:{_REDIS_PORT}/{_REDIS_DB}"
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": _REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# --- Celery (same redis instance, same DB index as CACHES above) ---
CELERY_BROKER_URL = _REDIS_URL
CELERY_RESULT_BACKEND = _REDIS_URL
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_TIMEZONE = TIME_ZONE

# --- Email ---
EMAIL_HOST = os.environ.get("EMAIL_HOST", "mailhog")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "1025"))
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", "0")

# --- Google OAuth ---
GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "")

# --- M-Pesa Daraja ---
MPESA_ENV = os.environ.get("MPESA_ENV", "sandbox")
MPESA_CONSUMER_KEY = os.environ.get("MPESA_CONSUMER_KEY", "")
MPESA_CONSUMER_SECRET = os.environ.get("MPESA_CONSUMER_SECRET", "")
MPESA_PAYBILL_NUMBER = os.environ.get("MPESA_PAYBILL_NUMBER", "")
MPESA_PASSKEY = os.environ.get("MPESA_PASSKEY", "")
MPESA_CALLBACK_URL = os.environ.get("MPESA_CALLBACK_URL", "")

# --- Firebase (FCM) ---
FCM_SERVER_KEY = os.environ.get("FCM_SERVER_KEY", "")