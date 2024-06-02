from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

from celery import shared_task


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_celery.settings')

#app = Celery('posts', broker='amqp://guest:**@localhost:5672//', backend='amqp://...', include=['posts.tasks'])

app = Celery('dj_celery')

app.config_from_object('django.conf:settings', namespace="CELERY")


app.autodiscover_tasks()