# usage: python manage.py test pjtk2 --settings=main.test_settings
# flake8: noqa
"""Settings to be used for running tests."""
import logging
import os

from main.settings.base import *


# eliminates naive error dates - not sure were the
USE_TZ = False


PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
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
