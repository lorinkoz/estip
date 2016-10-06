# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    name = 'apps.audit'
    verbose_name = 'Auditoría'

default_app_config = 'apps.audit.CustomAppConfig'



