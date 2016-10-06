# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from ...models import School


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        school = School.objects.first()
        if not school:
            School.objects.create(name='Universidad')
            self.stdout.write('School created!')
        else:
            self.stdout.write('School exists already!')
