# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        management.call_command('makeschool', interactive=False)
        management.call_command('makeadmin', interactive=False)
        fixtures = (
        	'faculty.json','specialty.json',
        	'student_type.json', 'payment_type.json',
        )
        management.call_command('loaddata', *fixtures, interactive=False)