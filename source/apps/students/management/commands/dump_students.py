# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, sys
from os.path import join, normpath, abspath
from django.core.management.base import BaseCommand, CommandError

from ...models import Student


class Command(BaseCommand):    
    help = 'Dumps all students in a custom format.'
    
    def handle(self, *args, **options):
        for student in Student.objects.exclude(status=None):
            stype = student.status.student_type.slug if student.status.student_type else ''
            data = (
                student.sid, student.name, student.surname, student.gender,
                student.status.year, student.status.specialty.slug, stype
            )
            self.stdout.write('{}|{}|{}|{}|{}|{}|{}'.format(*data))