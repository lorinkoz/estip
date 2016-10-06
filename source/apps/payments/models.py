# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.core.validators import ValidationError, MinValueValidator
from django.utils import six, timezone
from django.utils.encoding import python_2_unicode_compatible

from apps.core.models import PaymentType
from apps.students.models import Student
from common.abstracts import NamedModel
from common.constants import YEARS


class Payment(NamedModel):

    STATUS = (
        (0, 'No calculado'),
        (1, 'Calculando pagos'),
        (2, 'Listo'),
        (3, 'Cerrado'),
    )

    status = models.PositiveIntegerField(verbose_name='estado', choices=STATUS, default=0)
    description = models.TextField(verbose_name='descripción', blank=True)

    date_created = models.DateTimeField(verbose_name='fecha de apertura', auto_now_add=True)
    date_generated = models.DateTimeField(verbose_name='fecha de cálculo', blank=True, null=True)
    date_closed = models.DateTimeField(verbose_name='fecha de cierre', blank=True, null=True)

    generated_by = models.CharField(verbose_name='calculado por', max_length=512, blank=True)

    class Meta:
        verbose_name = 'pago'
        verbose_name_plural = 'pagos'
        ordering = ('-date_closed', 'date_created')

    def close(self):
        if self.can_close:
            self.date_closed = timezone.now()
            self.status = 3
            self.save()

    @property
    def is_pristine(self):
        return self.status == 0

    @property
    def in_process(self):
        return self.status == 1

    @property
    def is_ready(self):
        return self.status == 2

    @property
    def is_closed(self):
        return self.status == 3

    @property
    def can_close(self):
        return self.is_ready and not self.is_closed

    @property
    def can_generate(self):
        return self.is_pristine or self.is_ready

    @property
    def can_delete(self):
        return not self.in_process

    def generate(self, application_rules, author=''):
        if self.in_process:
            return False
        rows = {}
        if author:
            self.generated_by = author
        self.status = 1
        self.save()
        self.rows.all().delete()
        for student in Student.objects.exclude(status=None):
            rows[student] = PaymentRow(payment=self, student=student, year=student.status.year, specialty=student.status.specialty)
        PaymentRow.objects.bulk_create(rows.values())
        records = []
        for row in PaymentRow.objects.filter(payment=self):
            if row.student.status is None:
                continue # NOTE: This should never happen, as we have created them based on the same condition
            payment_dict = {}
            for rule in row.student.status.rules.all():
                payment_dict.setdefault(rule.payment_type, 0)
                payment_dict[rule.payment_type] += rule.amount * int(application_rules.get(rule.payment_type.slug, 0))
            for payment_type, amount in six.iteritems(payment_dict):
                if amount:
                    record = PaymentRecord(row=row, payment_type=payment_type, amount=amount)
                    records.append(record)
        PaymentRecord.objects.bulk_create(records)
        self.date_generated = timezone.now()
        self.status = 2
        self.save()
        return True

    def tabulate(self, student_filter='', limit=None):
        from .utils import tabulate_rows
        query_filters = \
            Q(name__icontains=student_filter) | \
            Q(surname__icontains=student_filter) | \
            Q(sid__iexact=student_filter)
        target_students = Student.objects.filter(query_filters)
        if limit:
            target_students = target_students[:limit]
        return tabulate_rows(PaymentRow.objects.filter(student__in=target_students, payment=self))


@python_2_unicode_compatible
class PaymentRow(models.Model):

    payment = models.ForeignKey('Payment', verbose_name='pago', related_name='rows')
    refunded = models.BooleanField(verbose_name='reintegrada', default=False)
    
    student = models.ForeignKey('students.Student', verbose_name='estudiante', related_name='rows')
    specialty = models.ForeignKey('core.Specialty', verbose_name='especialidad', related_name='rows')
    year = models.IntegerField(verbose_name='año que cursa', choices=YEARS, default=1)

    class Meta:
        verbose_name = 'fila de pago'
        verbose_name_plural = 'filas de pago'
        unique_together = ('payment', 'student')

    def __str__(self):
        return '%s / %s' % (self.payment, self.student)


@python_2_unicode_compatible
class PaymentRecord(models.Model):

    row = models.ForeignKey('PaymentRow', verbose_name='fila', related_name='records')

    payment_type = models.ForeignKey('core.PaymentType', verbose_name='tipo de pago', related_name='records')
    amount = models.DecimalField(verbose_name='monto a pagar', max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'registro de pago'
        verbose_name_plural = 'registros de pago'
        unique_together = ('row', 'payment_type')

    def __str__(self):
        return '%s / %s' % (self.row, self.payment_type)