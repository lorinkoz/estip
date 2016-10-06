# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import PaymentRecord
from apps.core.models import PaymentType


class PaymentTempRow(object):

    def __init__(self, payment, student, specialty, year, payments_count):
        self.payment = payment
        self.student = student
        self.specialty = specialty
        self.year = year
        self.payments = []
        for i in range(payments_count):
            self.payments.append(float(0.0))

    @property
    def total(self):
        return reduce(lambda x,y:x+float(y), self.payments, 0)


def tabulate_rows(rows):
    data = []
    iter_types = 0
    types = list(PaymentType.objects.filter(records__row__in=rows).distinct())
    temp_row = PaymentTempRow(None, None, None, None, len(types))
    ordering = (
        'row__payment__date_closed',
        'row__specialty__faculty',
        'row__specialty',
        'row__year',
        'row__student__sid',
        'payment_type'
    )
    related = ('row', 'row__payment', 'row__student', 'row__specialty', 'row__specialty__faculty', 'payment_type')
    for record in PaymentRecord.objects.filter(row__in=rows).select_related(*related).order_by(*ordering):
        if temp_row.student != record.row.student:
            data.append(temp_row)
            temp_row = PaymentTempRow(record.row.payment, record.row.student, record.row.specialty, '%s' % record.row.get_year_display(), len(types))
            iter_types = 0
        while types[iter_types] != record.payment_type:
            iter_types += 1
        temp_row.payments[iter_types] = record.amount
        iter_types += 1
    data.append(temp_row)
    if data and data[0].student is None:
        data.pop(0)
    return types, data