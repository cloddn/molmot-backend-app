from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.db.models import signals
from django.dispatch import receiver

from support.models import SupportNotification,SupportScheduledNotification
import json
import datetime


@receiver(signals.post_save, sender=SupportScheduledNotification)
def run_task_on_Support_save(sender, instance, created, **kwargs):
    noti_obj=SupportNotification.objects.get(pk=instance.sched_noti)
    noti_obj.crontab=instance.noti_on_time
    noti_obj.enabled=instance.noti_on_or_off
    noti_obj.date_changed=datetime.datetime.now()

