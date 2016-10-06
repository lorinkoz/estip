# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, sys
from os.path import join, normpath, abspath
from django.core.management.base import BaseCommand, CommandError

apache_template = '''
Alias /estipendio/robots.txt "%(robots_path)s"
Alias /estipendio/favicon.ico "%(favicon_path)s"

Alias /estipendio/static "%(static_path)s"
<Directory "%(static_path)s">
    Order Allow,Deny
    Allow from all
</Directory>

WSGIDaemonProcess estipendio python-path="%(project_path)s"
WSGIScriptAlias /estipendio "%(wsgi_path)s" process-group=estipendio application-group=%%{GLOBAL}

<Directory "%(wsgi_dir)s">
    <Files "wsgi.py">
        Order Allow,Deny
        Allow from all
    </Files>
</Directory>
'''

wsgi_template = '''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%(settings_path)s")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
'''


class Command(BaseCommand):    
    help = 'Creates a template configuration for apache.'
    
    def handle(self, *args, **options):
        from django.conf import settings
        verbosity = int(options.get('verbosity', 1))
        path = args[0] if len(args) else sys.path[0]
        deploy_folder = 'deploy_%s' % os.environ['DJANGO_SETTINGS_MODULE'].split('.')[-1]
        args = {
            'project_path': normpath(sys.path[0]),
            'static_path': normpath(settings.STATIC_ROOT),
            'robots_path': normpath(join(settings.STATIC_ROOT, 'robots.txt')),
            'favicon_path': normpath(join(settings.STATIC_ROOT, 'favicon.ico')),
            'wsgi_dir': normpath(abspath(join(path, deploy_folder))),
            'wsgi_path': normpath(abspath(join(path, deploy_folder, 'wsgi.py'))),
            'settings_path': os.environ['DJANGO_SETTINGS_MODULE'],
        }
        if not os.path.exists(join(path, deploy_folder)):
            os.mkdir(join(path, deploy_folder))
        with open(join(path, deploy_folder, 'apache.conf'), 'w') as file:
            file.write(apache_template % args)
            if verbosity: self.stdout.write('File apache.conf created.')
        with open(join(path, deploy_folder, 'wsgi.py'), 'w') as file:
            file.write(wsgi_template % args)
            if verbosity: self.stdout.write('File wsgi.py created.')