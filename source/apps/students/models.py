# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import ValidationError, RegexValidator
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible

from common.constants import YEARS

cid_validator = RegexValidator(r'\d{11}')


@python_2_unicode_compatible
class Student(models.Model):

    GENDERS = (
        ('m', 'Masculino'),
        ('f', 'Femenino'),
    )

    sid = models.PositiveIntegerField(verbose_name='código', unique=True)
    cid = models.CharField(verbose_name='carné de identidad', max_length=11, validators=[cid_validator], blank=True)

    name = models.CharField(verbose_name='nombres', max_length=512)
    surname = models.CharField(verbose_name='apellidos', max_length=512)
    gender = models.CharField(verbose_name='sexo', max_length=1, choices=GENDERS)

    status = models.OneToOneField('StudentStatus', verbose_name='estado', blank=True, null=True, on_delete=models.SET_NULL, related_name='student')
    linked_user = models.OneToOneField('users.User', verbose_name='usuario asociado', blank=True, null=True, on_delete=models.SET_NULL, related_name='student')

    class Meta:
        verbose_name = 'estudiante'
        verbose_name_plural = 'estudiantes'
        ordering = ('surname', 'name', 'sid')

    def __str__(self):
        return self.full_name

    def clean(self):
        self.name = self.name.strip()
        self.surname = self.surname.strip()

    def delete(self, *args, **kwargs):
        if self.status:
            self.status.delete()
        return super(Student, self).delete(*args, **kwargs)

    @property
    def full_name(self):
        return ' '.join([self.name, self.surname]).strip()

    @property
    def html_id(self):
        return '%d' % self.sid


@python_2_unicode_compatible
class StudentStatus(models.Model):

    student_type = models.ForeignKey('core.StudentType', verbose_name='tipo de estudiante', on_delete=models.SET_NULL, blank=True, null=True, related_name='students')

    specialty = models.ForeignKey('core.Specialty', verbose_name='especialidad', related_name='students')
    year = models.IntegerField(verbose_name='año que cursa', choices=YEARS, default=1)

    rules = models.ManyToManyField('core.PaymentRule', verbose_name='reglas de pago', blank=True, related_name='students_status')

    class Meta:
        verbose_name = 'estado de estudiante'
        verbose_name_plural = 'estados de estudiante'

    def __str__(self):
        return '{} de {}'.format(self.get_year_display(), self.specialty)

    def clean(self):
        if hasattr(self, 'specialty'):
            miny, maxy = self.specialty.year_range
            if not miny <= self.year <= maxy:
                raise ValidationError({'year': 'El año no es consistente con la especialidad seleccionada'})