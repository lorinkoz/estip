# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            User.objects.create_superuser('admin@localhost', 'Administrador', 'admin')
            self.stdout.write('Admin created!')
        except:
            self.stdout.write('Admin exists already!')