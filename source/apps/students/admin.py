# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from common.admin import myadmin

from . import models


@admin.register(models.Student, site=myadmin)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'surname')
    list_display = ('__str__', 'sid')


@admin.register(models.StudentStatus, site=myadmin)
class StudentStatusAdmin(admin.ModelAdmin):
    search_fields = ('student__name', 'student__surname')
    list_display = ('__str__', 'specialty', 'year')