from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.db.models import signals
from django.dispatch import receiver


from support.models import Support, SupportBookMark,SupportNotification,SupportScheduledNotification
import json
import datetime

from user.models import MemberFCMDevice

@receiver(signals.post_save, sender=Support) #Support 정보 수정하면 -> SupportNotification 수정하기.
def run_task_on_Support_save(sender, instance, created, **kwargs):
    try:
        #신청 날짜 지나면 마감 하루 일자 하루전 , 안지났으면 시작 일자 7일 동안 울리게 
        sched_noti=SupportNotification.objects.filter(pk=instance.start_date).update(
                noti_on_time=instance.start_date,
                crontab=instance.start_date,
                date_changed=datetime.datetime.now()
                )
    except SupportNotification.DoesNotExist:
        pass


#즐겨찾기 수정됐을때가 있나....?즐겨찾기 삭제될경우 -> 없어져야함.
@receiver(signals.post_save, sender=SupportBookMark) #즐겨찾기한 지원금 제도에 한정해서 추가되도록 
def run_task_on_SupportBookMark_save(sender, instance, created, **kwargs):
    try:
        #신청 날짜 지나면 마감 하루 일자 하루전 , 안지났으면 시작 일자 7일 동안 울리게 
        #기기 토큰 1개만 가지고 있을 수 있도록...?
        support_id=Support.objects.get(title=instance.support_id)
        member_device_info=MemberFCMDevice.objects.get(user=instance.member_id)
        SupportNotification.objects.get_or_create(member_device_info=member_device_info,support_id=support_id,noti_on_time=support_id.start_date)
    except Support.DoesNotExist or MemberFCMDevice.DoesNotExist:
        pass



