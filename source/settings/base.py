# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

path = lambda *x: os.path.join(BASE_DIR, *x)


BRAND_SHORT = 'Estipendio'
BRAND_LONG = 'Sistema de Estipendio'
VERSION = '2.0'

ADMINS = (('Lorenzo Peña', 'lorinkoz@vrea.uho.edu.cu'),)
MANAGERS = ADMINS


USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Havana'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'braces',
    'crispy_forms',
    'solo',

    'apps.core',
    'apps.students',
    'apps.payments',
    'apps.users',
    'apps.audit',
    'apps.setup',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'common.middleware.standard.ContextCompletionMiddleware',
    # 'common.middleware.ContextCompletionMiddleware',
    # 'common.middleware.FormDoubleSubmitProtectionMiddleware',
)

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'user_login'
LOGOUT_URL = 'user_logout'

ROOT_URLCONF = 'common.urls'

STATICFILES_DIRS = (
    path('static'),
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'common.context_processors.all',
            ],
        },
    },
]


LOCALE_PATHS = (
    path('locales'),
)

FORMAT_MODULE_PATH = 'formats'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
