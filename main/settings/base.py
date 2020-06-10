"""
Django settings for tfat project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# these are from Kennith Love's best practices
here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
root = lambda *x: os.path.join(os.path.abspath(BASE_DIR), *x)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "de79a-#kkh^go+p4z(4rkgn9#cy!6r!q66x09!1f#_zq*)owft"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.gis",
)

THIRDPARTY_APPS = (
    #    'djgeojson',
    "leaflet",
    "rest_framework",
    "django_filters",
    "myusers",
    "common",
)


MY_APPS = ("tfat",)

INSTALLED_APPS = DJANGO_APPS + THIRDPARTY_APPS + MY_APPS

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "../templates"),
            os.path.join(BASE_DIR, "../tfat/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "main.wsgi.application"

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE = "Canada/Eastern"

AUTH_USER_MODEL = "myusers.CustomUser"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)


# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_mails')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../media/"))
# print("MEDIA_ROOT = " + MEDIA_ROOT)

STATIC_URL = "/static/"
STATIC_ROOT = root("static/")
STATICFILES_DIRS = (os.path.abspath(os.path.join(BASE_DIR, "../static")),)

# print("STATIC_ROOT = " + STATIC_ROOT)
# print("STATICFILE_DIRS = " + STATICFILES_DIRS)

LEAFLET_CONFIG = {
    # minx, miny, maxx,maxy
    #'SPATIAL_EXTENT': (-84.0, 43.0,-80.0, 47.0),
    "DEFAULT_CENTER": (45.0, -82.0),
    "DEFAULT_ZOOM": 8,
    #'MIN_ZOOM': 3,
    #'MAX_ZOOM': 18,
    "RESET_VIEW": True,
}

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",)
}

GEOS_LIBRARY_PATH = "c:/OSGeo4W/bin/geos_c.dll"
GDAL_LIBRARY_PATH = "C:/OSGeo4W/bin/gdal300.dll"
