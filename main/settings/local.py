from main.settings.base import *

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, '../db/tfat.db'),
#    }
# }

#
# DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.postgresql_psycopg2",
#        "NAME": "tfat",
#        "USER": "cottrillad",
#        "PASSWORD": "django123",
#        "HOST": "localhost",
#    }
# }
#

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": "142.143.160.56",
        "NAME": "tfat",
        "USER": "cottrillad",
        "PASSWORD": "django",
    }
}


INSTALLED_APPS += (
    "debug_toolbar",
    "django_extensions",
    #'werkzeug_debugger_runserver',
)
#
# INTERNAL_IPS = ('127.0.0.1', )   #added for debug toolbar
#
# def show_toolbar(request):
#    return True
# SHOW_TOOLBAR_CALLBACK = show_toolbar

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
