
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_celery.settings')

#app = Celery('posts', broker='amqp://guest:**@localhost:5672//', backend='amqp://...', include=['posts.tasks'])

app = Celery('dj_celery')

app.config_from_object('django.conf:settings', namespace="CELERY")


app.autodiscover_tasks() 

""" 

from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp

app = TenantAwareCeleryApp()
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


 """








""" 
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp
from django.conf import settings

from celery import shared_task


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_celery.settings')

#app = Celery('posts', broker='amqp://guest:**@localhost:5672//', backend='amqp://...', include=['posts.tasks'])


app = TenantAwareCeleryApp('dj_celery')
#app = Celery('dj_celery')

app.config_from_object('django.conf:settings', namespace="CELERY")


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

 """