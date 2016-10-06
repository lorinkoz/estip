# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *


DEBUG = False

BRAND_SHORT = BRAND_SHORT + ' -stg-'

ALLOWED_HOSTS = ['10.26.16.8']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'estip',
        'USER': 'estip',
        'PASSWORD': 'stagingestip',
        'HOST': '',
        'PORT': '',
    },
}

AUTHENTICATION_BACKENDS = (
	'apps.users.backends.OpenLdapUHOBackend',
	'django.contrib.auth.backends.ModelBackend',
)

STATIC_URL = '/estipendio/static/'
STATIC_ROOT = path('../storage/static/')

MEDIA_URL = '/estipendio/media/'
MEDIA_ROOT = path('../storage/media/')

SECRET_KEY = 'n&aksdjajsdfjakjdf8ajdioqj904jfklasd8fa/gf.h,b'
