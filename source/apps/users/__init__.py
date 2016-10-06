# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    name = 'apps.users'
    verbose_name = 'Usuarios'

default_app_config = 'apps.users.CustomAppConfig'



