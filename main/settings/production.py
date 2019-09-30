from main.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '142.143.160.56',
        'NAME': 'tfat',
        'USER': 'cottrillad',
        'PASSWORD': 'django',
    }
}


STATIC_ROOT = root("../static/")
