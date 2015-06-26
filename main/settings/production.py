from main.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

DB_FILE = os.path.abspath(os.path.join(BASE_DIR, '../db/tfat.db')),

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_FILE[0],
    }
}




#DATABASES = {
#    'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'pjtk2',
#         'USER': 'adam',
#         'PASSWORD': 'django',
#     }
#}
