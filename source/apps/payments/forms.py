# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from . import models
from apps.core.models import PaymentType


class PaymentGenerationForm(forms.Form):

	OPTIONS = (
		(0, 'No aplicar'),
		(1, 'Aplicar normalmente'),
		(2, 'Aplicar al doble'),
		(3, 'Aplicar al triple'),
	)

	def __init__(self, *args, **kwargs):
		super(PaymentGenerationForm, self).__init__(*args, **kwargs)
		for payment_type in PaymentType.objects.filter(allow_rules=True):
			kwargs = {
				'label': payment_type.name,
				'choices': PaymentGenerationForm.OPTIONS,
				'initial': payment_type.regularity,
			}
			self.fields[payment_type.slug] = forms.ChoiceField(**kwargs)


class PaymentRecordsForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(PaymentRecordsForm, self).__init__(*args, **kwargs)
		for payment_type in PaymentType.objects.all():
			kwargs = {
				'label': payment_type.name,
				'max_digits': 20,
				'decimal_places': 2,
				'initial': 0,
			}
			self.fields[payment_type.slug] = forms.DecimalField(**kwargs)