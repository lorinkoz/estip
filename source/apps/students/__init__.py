# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    name = 'apps.students'
    verbose_name = 'Estudiantes'

default_app_config = 'apps.students.CustomAppConfig'



