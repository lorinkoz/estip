# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib.staticfiles.views import serve
from .admin import myadmin


def admin_pattern():
    from hashlib import md5
    from django.conf import settings
    from django.utils import timezone
    now = timezone.now()
    hash = '/' + md5('{}-{}'.format(settings.BRAND_SHORT, now.date())).hexdigest() if not settings.DEBUG else ''
    return r'^admin{}/'.format(hash)


urlpatterns = [
    url(r'^', include('apps.core.urls')),
    url(r'^', include('apps.students.urls')),
    url(r'^', include('apps.payments.urls')),
    url(r'^', include('apps.users.urls')),
    url(admin_pattern(), include(myadmin.urls)),
]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve),
]
