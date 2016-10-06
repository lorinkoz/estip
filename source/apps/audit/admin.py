# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from common.admin import myadmin

from . import models


@admin.register(models.Trace, site=myadmin)
class TraceAdmin(admin.ModelAdmin):
    pass
