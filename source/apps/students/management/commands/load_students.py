# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, sys
from os.path import join, normpath, abspath
from django.core.management.base import BaseCommand, CommandError

from ...models import Student, StudentStatus
from apps.core.models import Specialty, StudentType


class Command(BaseCommand):    
    help = 'Loads all students from a custom format.'
    
    def handle(self, *args, **options):
        while True:
            line = ''
            try:
                line = raw_input().strip()
            except:
                pass
            if not line:
                break
            try:
                self.stdout.write(line)
                sid, name, surname, gender, year, specialty, student_type = line.split('|')
                sta = StudentStatus.objects.create(specialty=Specialty.objects.get(slug=specialty), student_type=StudentType.objects.filter(slug=student_type).first(), year=int(year))
                s = Student.objects.create(sid=sid, name=name, surname=surname, gender=gender, status=sta)
            except Exception as e:
                continue
        self.stdout.write('Done!')