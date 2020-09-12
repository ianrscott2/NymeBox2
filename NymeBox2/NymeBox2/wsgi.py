"""
WSGI config for NymeBox2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

WSGI_FILE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(WSGI_FILE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NymeBox2.settings')
sys.path.append(WSGI_FILE_DIR)
sys.path.append('/usr/lib/python3/dist-packages')

application = get_wsgi_application()
