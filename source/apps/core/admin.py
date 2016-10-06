# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from solo.admin import SingletonModelAdmin

from common.admin import myadmin

from . import models


@admin.register(models.School, site=myadmin)
class SchoolAdmin(SingletonModelAdmin):
    pass


@admin.register(models.Faculty, site=myadmin)
class FacultyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    readonly_fields = ('slug',)


@admin.register(models.Specialty, site=myadmin)
class SpecialtyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    readonly_fields = ('slug',)


@admin.register(models.StudentType, site=myadmin)
class StudentTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    readonly_fields = ('slug',)


@admin.register(models.PaymentType, site=myadmin)
class PaymentTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    readonly_fields = ('slug',)


@admin.register(models.PaymentRule, site=myadmin)
class PaymentRuleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'amount')
    readonly_fields = ('slug',)