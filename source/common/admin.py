# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.admin.sites import AdminSite as DefaultAdminSite


class AdminSite(DefaultAdminSite):
    site_title = settings.BRAND_SHORT
    site_header = settings.BRAND_LONG
    index_title = 'Sitio de administración'


myadmin = AdminSite()
