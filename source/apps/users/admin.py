# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from common.admin import myadmin

from . import models, forms


@admin.register(models.User, site=myadmin)
class UserAdmin(DefaultUserAdmin):
    form = forms.AdminUserChangeForm
    add_form = forms.AdminUserCreationForm
    list_display = ('email', 'display_name', 'role',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        ('información básica', {'fields': ('email', 'display_name')}),
        ('información de seguridad', {'fields': ('password', 'role')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
    )
