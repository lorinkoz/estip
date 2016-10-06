# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import ValidationError, MinValueValidator
from django.utils.encoding import python_2_unicode_compatible

from solo.models import SingletonModel

from common.abstracts import NamedModel


class School(SingletonModel, NamedModel):

    logo = models.ImageField(verbose_name='logo', upload_to='logos', blank=True)

    class Meta:
        verbose_name = 'universidad'


class Faculty(NamedModel):

    class Meta:
        verbose_name = 'facultad'
        verbose_name_plural = 'facultades'


class Specialty(NamedModel):

    STRUCTURES = (
        ('0:5', 'Cinco años con preparatoria'),
        ('1:4', 'Cuatro años'),
        ('1:5', 'Cinco años'),
        ('1:6', 'Seis años'),
    )

    faculty = models.ForeignKey('Faculty', verbose_name='facultad', related_name='specialties')
    structure = models.CharField(verbose_name='estructura de años', max_length=3, choices=STRUCTURES, default='1:5')

    class Meta:
        verbose_name = 'especialidad'
        verbose_name_plural = 'especialidades'

    @property
    def year_range(self):
        return [int(x) for x in self.structure.split(':')]

    @property
    def min_year(self):
        miny, maxy = self.structure.split(':')
        return int(miny)

    @property
    def max_year(self):
        miny, maxy = self.structure.split(':')
        return int(maxy)


class StudentType(NamedModel):

    class Meta:
        verbose_name = 'tipo de estudiante'
        verbose_name_plural = 'tipos de estudiante'


class PaymentType(NamedModel):

    REGULARITY = (
        (0, 'Ocasional'),
        (1, 'Frecuente'),
    )

    ordering = models.PositiveIntegerField(verbose_name='ordernamiento', default=0)
    alias = models.CharField(verbose_name='alias', max_length=5, blank=True)

    regularity = models.PositiveIntegerField(verbose_name='regularidad', choices=REGULARITY, default=1)
    allow_rules = models.BooleanField(verbose_name='permite reglas de pago', default=False)

    class Meta:
        verbose_name = 'tipo de pago'
        verbose_name_plural = 'tipos de pago'
        ordering = ('ordering', 'slug')

    def get_alias(self):
        return self.alias.strip().upper() or self.slug[:5].upper()

    def save(self, *args, **kwargs):
        super(PaymentType, self).save(*args, **kwargs)
        if not self.ordering:
            self.ordering = self.pk
            super(PaymentType, self).save(*args, **kwargs)


@python_2_unicode_compatible
class PaymentRule(NamedModel):

    payment_type = models.ForeignKey('PaymentType', verbose_name='tipo de pago', limit_choices_to={'allow_rules': True}, related_name='rules')

    amount = models.DecimalField(verbose_name='monto a pagar', max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(verbose_name='descripción', blank=True)

    class Meta:
        verbose_name = 'regla de pago'
        verbose_name_plural = 'reglas de pago'
        ordering = ('payment_type', 'amount')

    def __str__(self):
        return '{} ({})'.format(self.name, self.amount)
