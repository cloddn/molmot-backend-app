import django
from celery.utils.log import get_task_logger
import datetime
logger = get_task_logger(__name__)

django.setup()

from celery import shared_task

@shared_task
def support_notification_push(*args, **kwargs):
   print("푸시알림 정해진대로 전송")