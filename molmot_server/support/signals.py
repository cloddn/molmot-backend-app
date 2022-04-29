from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.db.models import signals
from django.dispatch import receiver


from support.models import Support,SupportNotification,SupportScheduledNotification
import json
import datetime

@receiver(signals.post_save, sender=Support) #Support 정보 수정하면 -> SupportNotification 수정하기.
def run_task_on_Support_save(sender, instance, created, **kwargs):
    noti_obj=SupportNotification.objects.get(pk=instance.sched_noti)
    noti_obj.crontab=instance.noti_on_time
    noti_obj.enabled=instance.noti_on_or_off
    noti_obj.date_changed=datetime.datetime.now()



@receiver(signals.post_save, sender=SupportNotification)
def run_task_on_Support_save(sender, instance, created, **kwargs):
    noti_obj=SupportNotification.objects.get(pk=instance.sched_noti)
    noti_obj.crontab=instance.noti_on_time
    noti_obj.enabled=instance.noti_on_or_off
    noti_obj.date_changed=datetime.datetime.now()

