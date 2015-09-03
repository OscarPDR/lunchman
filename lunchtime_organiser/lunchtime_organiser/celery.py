
from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lunchtime_organiser.settings.local')
except:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lunchtime_organiser.settings.prod')

from django.conf import settings

app = Celery('lunchtime_organiser')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
