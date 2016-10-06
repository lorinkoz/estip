# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from common.admin import myadmin

from . import models


@admin.register(models.Payment, site=myadmin)
class PaymentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'date_created', 'date_closed')


@admin.register(models.PaymentRow, site=myadmin)
class PaymentRowAdmin(admin.ModelAdmin):
    search_fields = ('payment', 'student')
    list_display = ('payment', 'student')


@admin.register(models.PaymentRecord, site=myadmin)
class PaymentRecordAdmin(admin.ModelAdmin):
    search_fields = ('row', 'payment_type')
    list_display = ('row', 'payment_type')
