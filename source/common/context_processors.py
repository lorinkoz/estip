# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


def constants(request):
    return {
        'BRAND_SHORT': settings.BRAND_SHORT,
        'BRAND_LONG': settings.BRAND_LONG,
    }


def payments(request):
	from apps.payments.models import Payment
	return {
		'current_payment': Payment.objects.filter(date_closed=None).first()
	}


def all(request):
	base = {}
	for func in [constants, payments]:
		base.update(func(request))
	return base