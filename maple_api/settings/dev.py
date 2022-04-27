from .common import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@xe85@$xkdzt=$tw1h@cevoj*c-@)s4yqe^u*&39uta41rwz#8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.environ.get('DJANGO_MYSQL_DB_NAME'),
#         'HOST': 'localhost',
#         'USER': 'root',
#         'PASSWORD': os.environ.get('DJANGO_MYSQL_DB_PASSWORD'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DJANGO_MYSQL_DB_NAME'),
        'HOST': 'localhost',
        'USER': 'postgres',
        'PORT': 5432,
        'PASSWORD': os.environ.get('DJANGO_MYSQL_DB_PASSWORD'),
    }
}
