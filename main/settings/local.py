from main.settings.base import *

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        # "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "tfat",
        "USER": "cottrillad",
        "PASSWORD": "django",
        "HOST": "localhost",
    }
}


INSTALLED_APPS += (
    "debug_toolbar",
    "django_extensions",
    #'werkzeug_debugger_runserver',
)
#
INTERNAL_IPS = ("127.0.0.1",)  # added for debug toolbar
#
# def show_toolbar(request):
#    return True
# SHOW_TOOLBAR_CALLBACK = show_toolbar

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
