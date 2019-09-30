# usage: python manage.py test pjtk2 --settings=main.test_settings
# flake8: noqa
"""Settings to be used for running tests."""
import logging
import os

from main.settings.base import *


PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)


# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': ':memory:',
#    }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "tfat",
        "USER": "cottrillad",
        "PASSWORD": "django123",
        "HOST": "localhost",
    }
}


# COVERAGE_MODULE_EXCLUDES = [
#    'tests$', 'settings$', 'urls$', 'locale$',
#    'migrations', 'fixtures', 'admin$', 'django_extensions',
# ]
# COVERAGE_MODULE_EXCLUDES += THIRDPARTY_APPS + DJANGO_APPS
# COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(__file__, '../../../coverage')

logging.getLogger("factory").setLevel(logging.WARN)
