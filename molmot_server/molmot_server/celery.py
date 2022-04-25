from __future__ import absolute_import, unicode_literals
import sys
from kombu.utils import encoding
sys.modules['celery.utils.encoding'] = encoding

import os, django
from celery import Celery
from datetime import timedelta
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'molmot_server.settings')

app = Celery('molmot_server', include=['support.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler',
)

django.setup()


app.autodiscover_tasks()
if __name__ == '__main__':
    app.start()

@app.task(bind=True)
def debug_task(self):
   print('Request: {0!r}'.format(self.request))