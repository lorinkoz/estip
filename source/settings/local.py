# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *


DEBUG = True

BRAND_SHORT = BRAND_SHORT + ' -dev-'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'estip',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
    },
}

STATIC_URL = '/static/'
STATIC_ROOT = path('../storage/static/')
STATICFILES_DIRS = STATICFILES_DIRS + (
    path('../storage/'),
)

MEDIA_URL = '/static/media/'
MEDIA_ROOT = path('../storage/media/')

INTERNAL_IPS = ('127.0.0.1',)
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'JQUERY_URL': None,
}

SECRET_KEY = 'n&jlads98f7ajdklfaj8sdfoasdof8akd38yasdhftvb'
