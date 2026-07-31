from .base import *  # noqa: F401,F403

DEBUG = True

# Django's browsable API + admin are handy in dev
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]