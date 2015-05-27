from main.settings.base import *

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db/tfat.db'),
    }
}

#MIDDLEWARE_CLASSES += (
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
#)
#
#INSTALLED_APPS += (
#    'debug_toolbar',
#    'django_extensions',
#    #'werkzeug_debugger_runserver',
#
#)
#
#INTERNAL_IPS = ('127.0.0.1', )   #added for debug toolbar
#
#def show_toolbar(request):
#    return True
#SHOW_TOOLBAR_CALLBACK = show_toolbar
