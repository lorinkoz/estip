# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    name = 'apps.payments'
    verbose_name = 'Pagos'

default_app_config = 'apps.payments.CustomAppConfig'



