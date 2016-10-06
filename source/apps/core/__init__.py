# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    name = 'apps.core'
    verbose_name = 'Catálogos'

default_app_config = 'apps.core.CustomAppConfig'



