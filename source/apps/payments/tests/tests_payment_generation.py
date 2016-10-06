# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.test import TestCase

from ..models import Payment, PaymentRecord
from apps.core.models import Specialty, PaymentType, PaymentRule
from apps.students.models import Student, StudentStatus


class PaymentGenerationTestCase(TestCase):
    fixtures = (
        'faculty.json',
        'specialty.json',
        'payment_type.json',
    )
    
    def setUp(self):
        specialty = Specialty.objects.order_by('?').first()
        self.student = Student.objects.create(sid=1, name='Juan', surname='Pérez', gender='M', status=StudentStatus.objects.create(specialty=specialty, year=specialty.min_year))
        self.payment_type = PaymentType.objects.order_by('?').first()
        self.payment_type2 = PaymentType.objects.exclude(pk=self.payment_type.pk).order_by('?').first()
        self.amount = random.randrange(50, 100, step=10)
        self.amount2 = random.randrange(50, 100, step=10)
        self.student.status.rules = [
            PaymentRule.objects.create(payment_type=self.payment_type, amount=self.amount),
            PaymentRule.objects.create(payment_type=self.payment_type2, amount=self.amount2),
        ]
        self.payment = Payment.objects.create(name='Sample Payment')

    def test_overall_payment_generation(self):
        application_rules = {self.payment_type.slug: 1}
        self.payment.generate(application_rules)
        record = PaymentRecord.objects.first()
        record_count = PaymentRecord.objects.count()
        self.assertTrue(record)
        self.assertEqual(record_count, 1)
        self.assertEqual(record.row.student, self.student)
        self.assertEqual(record.payment_type, self.payment_type)
        self.assertEqual(record.amount, self.amount)
    
    def test_empty_payment(self):
        application_rules = {self.payment_type.slug: 0}
        self.payment.generate(application_rules)
        record = PaymentRecord.objects.first()
        self.assertEqual(record, None)
    
    def test_double_payment(self):
        application_rules = {self.payment_type.slug: 2}
        self.payment.generate(application_rules)
        record = PaymentRecord.objects.first()
        self.assertEqual(record.amount, self.amount * 2)
    
    def test_triple_payment(self):
        application_rules = {self.payment_type.slug: 3}
        self.payment.generate(application_rules)
        record = PaymentRecord.objects.first()
        self.assertEqual(record.amount, self.amount * 3)
    
    def test_combined_payments(self):
        application_rules = {self.payment_type.slug: 1, self.payment_type2.slug: 2}
        self.payment.generate(application_rules)
        self.assertTrue(PaymentRecord.objects.filter(payment_type=self.payment_type, amount=self.amount).first())
        self.assertTrue(PaymentRecord.objects.filter(payment_type=self.payment_type2, amount=self.amount2*2).first())
        self.assertEqual(PaymentRecord.objects.count(), 2)
    
    
        