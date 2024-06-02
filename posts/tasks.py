from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task(name='add')
def add(x, y):
    return x + y

print(add.delay(4, 5))