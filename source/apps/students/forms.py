# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.db.models import Count

from . import models
from apps.core.models import Specialty, StudentType, PaymentType, PaymentRule
from common.constants import YEARS
from common.snippets import multicat


class StudentForm(forms.ModelForm):

	class Meta:
		model = models.Student
		fields = ('name', 'surname', 'sid', 'gender', 'cid')


class StudentStatusForm(forms.ModelForm):

	class Meta:
		model = models.StudentStatus
		fields = ('student_type', 'specialty', 'year', 'rules')
		widgets = {
			'rules': multicat.PartitionSelectMultiple(
				empty_label='[Sin {}]',
				attrs={'class': 'form-control'},
				partition_function=lambda x: [(y, y.payment_type) for y in PaymentRule.objects.filter(pk__in=x).select_related('payment_type')],
			),
		}


class StudentFilterForm(forms.Form):

	q = forms.CharField(label='Nombre', required=False)
	sp = forms.ModelChoiceField(label='Especialidad', queryset=Specialty.objects.all(), required=False, empty_label='Cualquier especialidad')
	yr = forms.ChoiceField(label='Año que cursa', choices=(('', 'Cualquier año'),) + YEARS, required=False)
	ty = forms.ModelChoiceField(label='Tipo de estudiante', queryset=StudentType.objects.all(), required=False, empty_label='Cualquier tipo de estudiante')
	rl = forms.ModelChoiceField(label='Con regla de pago', queryset=PaymentRule.objects.all(), required=False, empty_label='Cualquier regla de pago')

	def filter(self, qs):
		from django.db.models import Q
		self.is_filtered = 0
		if not self.is_valid():
			return
		q = self.cleaned_data['q'].strip()
		student_type = self.cleaned_data['ty']
		specialty = self.cleaned_data['sp']
		year = self.cleaned_data['yr']
		rule = self.cleaned_data['rl']
		if q:
			qs = qs.filter(Q(name__icontains=q)|Q(surname__icontains=q)|Q(sid__iexact=q))
			self.is_filtered += 1
		if student_type:
			qs = qs.filter(status__student_type=student_type)
			self.is_filtered += 1
		if specialty:
			qs = qs.filter(status__specialty=specialty)
			self.is_filtered += 1
		if year:
			qs = qs.filter(status__year=year)
			self.is_filtered += 1
		if rule:
			qs = qs.filter(status__rules=rule).distinct()
			self.is_filtered += 1
		return qs


class StudentPromoteForm(forms.Form):

	exceptions = forms.ModelMultipleChoiceField(label='No promover a estos estudiantes', queryset=models.Student.objects.exclude(status=None), required=False)


class StudentRulesTransformForm(forms.Form):

	student_type = forms.ModelChoiceField(label='Tipo de estudiante', queryset=StudentType.objects.all(), empty_label='Cualquier tipo de estudiante', required=False)
	specialty = forms.ModelChoiceField(label='Especialidad', queryset=Specialty.objects.all(), empty_label='Cualquier especialidad', required=False)
	year = forms.ChoiceField(label='Año que cursa', choices=(('', 'Cualquier año'),) + YEARS, required=False)

	current_rules = forms.ModelMultipleChoiceField(label='Reglas actuales', queryset=PaymentRule.objects.all(),
		required=False, widget=multicat.PartitionSelectMultiple(
				empty_label='[Cualquier regla de {}]',
				attrs={'class': 'form-control'},
				partition_function=lambda x: [(y, y.payment_type) for y in PaymentRule.objects.filter(pk__in=x).select_related('payment_type')],
			))

	transformed_rules = forms.MultipleChoiceField(label='Reglas transformadas',
		choices=[],
		required=False, widget=multicat.PartitionSelectMultiple(
				empty_label='[Mantener regla para {}]',
				attrs={'class': 'form-control'},
				partition_function=lambda x: [(y, y.payment_type) for y in PaymentRule.objects.filter(pk__in=x).select_related('payment_type')] + [(-y.pk, y) for y in PaymentType.objects.annotate(rule_count=Count('rules')).filter(rule_count__gt=0, allow_rules=True)],
			))

	def __init__(self, *args, **kwargs):
	    super(StudentRulesTransformForm, self).__init__(*args, **kwargs)
	    self.fields['transformed_rules'].choices = [(x.pk, x) for x in PaymentRule.objects.all()] + [(-x.pk, '[Eliminar regla para {}]'.format(x)) for x in PaymentType.objects.annotate(rule_count=Count('rules')).filter(rule_count__gt=0, allow_rules=True)]